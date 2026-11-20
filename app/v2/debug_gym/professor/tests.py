# [Professor Dev] Regression checks for dashboard role access
import json

from django.test import TestCase

from core.models import User
from datetime import timedelta
from io import BytesIO
from zipfile import ZipFile
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError, transaction
from django.urls import reverse
from django.utils import timezone

from core.models import Assignment, Bug, StudyGroup, Submission


class DashboardAccessTests(TestCase):
    def test_professor_can_open_dashboard(self):
        user = User.objects.create_user(
            "professor@example.com", "Professor", role=User.Role.PROFESSOR,
        )
        self.client.force_login(user)
        self.assertEqual(self.client.get("/professor/").status_code, 200)

    def test_other_roles_are_denied(self):
        for role in (User.Role.STUDENT, User.Role.ADMIN):
            with self.subTest(role=role):
                user = User.objects.create_user(f"{role}@example.com", role, role=role)
                self.client.force_login(user)
                self.assertEqual(self.client.get("/professor/").status_code, 403)

    def test_signed_out_visitor_is_redirected_to_login(self):
        self.assertRedirects(
            self.client.get("/professor/"), "/accounts/login/?next=/professor/",
        )


class TeachingWorkflowTests(TestCase):
    def setUp(self):
        verifier = patch("student.views.verify", return_value=(1, 1))
        verifier.start()
        self.addCleanup(verifier.stop)
        self.teacher = User.objects.create_user("teacher@example.com", "Teacher", role="professor")
        self.other = User.objects.create_user("other@example.com", "Other teacher", role="professor")
        self.student = User.objects.create_user("student@example.com", "Student Full Name")
        self.group = StudyGroup.objects.create(name="My group", professor=self.teacher)
        self.group.students.add(self.student)
        self.foreign_group = StudyGroup.objects.create(name="Foreign group", professor=self.other)
        self.bug = Bug.objects.create(
            title="My private exercise", description="Find the bug", buggy_code="return 0",
            solution_code="return 1", language="python", difficulty="easy",
            visibility="private", created_by=self.teacher,
        )
        self.foreign_bug = Bug.objects.create(
            title="Foreign private exercise", description="Private", buggy_code="x",
            solution_code="y", language="python", difficulty="easy", visibility="private",
            created_by=self.other,
        )
        self.public = Bug.objects.create(
            title="Public exercise", description="Public", buggy_code="x", solution_code="y",
            language="python", difficulty="easy", visibility="public", created_by=self.other,
        )
        self.client.force_login(self.teacher)

    def assignment(self, deadline=None, group=None):
        assignment = Assignment.objects.create(
            title="Assigned bug", bug=self.bug, professor=self.teacher, deadline=deadline,
        )
        assignment.groups.add(group or self.group)
        return assignment

    def assignment_url(self, name, assignment, group=None):
        return reverse(f"professor:{name}", args=[(group or self.group).pk, assignment.pk])

    def test_only_owned_groups_and_students_are_visible(self):
        response = self.client.get(reverse("professor:dashboard"))
        self.assertContains(response, "My group")
        self.assertNotContains(response, "Foreign group")
        page = self.client.get(reverse("professor:group", args=[self.group.pk]))
        self.assertContains(page, self.student.email)
        self.assertEqual(
            self.client.get(reverse("professor:group", args=[self.foreign_group.pk])).status_code, 404,
        )

    def test_assignments_have_independent_optional_deadlines(self):
        second = StudyGroup.objects.create(name="Second group", professor=self.teacher)
        deadline = (timezone.now() + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M")
        for group, due in ((self.group, ""), (second, deadline)):
            response = self.client.post(reverse("professor:assign", args=[group.pk]), {
                "bug": self.bug.pk, "title": "Assignment", "deadline": due,
            })
            self.assertRedirects(response, reverse("professor:group", args=[group.pk]))
        first = self.group.assignments.get()
        other = second.assignments.get()
        self.assertIsNone(first.deadline)
        self.assertIsNotNone(other.deadline)
        self.client.post(self.assignment_url("assignment", first), {"deadline": deadline})
        other.refresh_from_db()
        self.assertEqual(other.deadline.strftime("%Y-%m-%dT%H:%M"), deadline)

    def test_cannot_assign_foreign_private_bug_or_group(self):
        response = self.client.post(reverse("professor:assign", args=[self.group.pk]), {
            "bug": self.foreign_bug.pk, "title": "Bad assignment",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(Assignment.objects.count(), 0)
        response = self.client.post(reverse("professor:assign", args=[self.foreign_group.pk]), {
            "bug": self.public.pk, "title": "Bad group",
        })
        self.assertEqual(response.status_code, 404)

    def test_catalog_visibility_and_publication_ownership(self):
        page = self.client.get(reverse("professor:bugs"))
        self.assertContains(page, self.bug.title)
        self.assertContains(page, self.public.title)
        self.assertNotContains(page, self.foreign_bug.title)
        self.assertEqual(self.client.post(
            reverse("professor:publish", args=[self.foreign_bug.pk]),
        ).status_code, 404)
        self.assertEqual(self.client.get(
            reverse("professor:publish", args=[self.bug.pk]),
        ).status_code, 405)
        self.client.post(reverse("professor:publish", args=[self.bug.pk]))
        self.bug.refresh_from_db()
        self.assertEqual(self.bug.visibility, "public")

    def test_foreign_public_exercise_is_read_only_in_page_and_workspace(self):
        self.public.solution_code = "secret reference implementation"
        self.public.save()
        url = reverse("professor:bug", args=[self.public.pk])
        page = self.client.get(url)
        self.assertContains(page, "read-only")
        self.assertNotContains(page, "Save details")
        self.assertNotContains(page, self.public.solution_code)
        self.assertNotContains(page, "Save project")
        self.assertEqual(self.client.post(url, {
            "title": "Forged", "description": "Forged", "difficulty": "easy",
            "revision": self.public.revision,
        }).status_code, 404)
        self.assertEqual(self.client.post(
            reverse("workspace-launch", args=[self.public.pk]), {"mode": "author"},
        ).status_code, 403)
        for action in ("publish", "unpublish"):
            self.assertEqual(self.client.post(
                reverse(f"professor:{action}", args=[self.public.pk]),
            ).status_code, 404)
        self.public.refresh_from_db()
        self.assertEqual(self.public.title, "Public exercise")
        self.assertEqual(self.public.visibility, "public")

    def test_owner_can_unpublish_without_removing_assignment_access(self):
        assignment = self.assignment()
        self.client.post(reverse("professor:publish", args=[self.bug.pk]))
        url = reverse("professor:unpublish", args=[self.bug.pk])
        self.assertContains(self.client.get(reverse("professor:bugs")), f'action="{url}"')
        self.assertContains(self.client.get(reverse("professor:bug", args=[self.bug.pk])), "Unpublish")
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertRedirects(self.client.post(url), reverse("professor:bugs"))
        self.bug.refresh_from_db()
        self.assertEqual(self.bug.visibility, "private")
        self.client.force_login(self.other)
        self.assertNotContains(self.client.get(reverse("professor:bugs")), self.bug.title)
        self.client.force_login(self.student)
        self.assertEqual(self.client.get(
            reverse("student:assignment_detail", args=[assignment.pk]),
        ).status_code, 200)

    def test_foreign_public_assignment_copies_project_and_links_original(self):
        self.public.project_files = {"src/main.py": "broken", "tests/test_main.py": "test"}
        self.public.entry_file = "src/main.py"
        self.public.compose_config = "services: {}"
        self.public.revision = 7
        self.public.save()
        deadline = (timezone.now() + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M")
        response = self.client.post(reverse("professor:assign", args=[self.group.pk]), {
            "bug": self.public.pk, "title": "Copied assignment", "deadline": deadline,
        })
        self.assertRedirects(response, reverse("professor:group", args=[self.group.pk]))
        assignment = self.group.assignments.get()
        copy = assignment.bug
        self.assertNotEqual(copy.pk, self.public.pk)
        self.assertEqual(copy.created_by, self.teacher)
        self.assertEqual(copy.visibility, "private")
        self.assertEqual(copy.revision, 1)
        for field in ("title", "buggy_code", "solution_code", "language", "difficulty",
                      "project_files", "entry_file", "compose_config"):
            self.assertEqual(getattr(copy, field), getattr(self.public, field), field)
        source_url = "http://testserver" + reverse("professor:bug", args=[self.public.pk])
        self.assertEqual(copy.description, f"{self.public.description}\n\nCopied from: {source_url}")
        page = self.client.get(reverse("professor:bug", args=[copy.pk]))
        self.assertContains(page, f'href="{source_url}"')
        self.assertEqual(assignment.deadline.strftime("%Y-%m-%dT%H:%M"), deadline)
        self.assertEqual(assignment.professor, self.teacher)
        self.public.project_files = {"main.py": "changed by original author"}
        self.public.visibility = "private"
        self.public.save()
        copy.refresh_from_db()
        self.assertEqual(copy.project_files["src/main.py"], "broken")
        self.client.force_login(self.student)
        self.assertEqual(self.client.get(
            reverse("student:assignment_detail", args=[assignment.pk]),
        ).status_code, 200)

    def test_own_public_exercise_is_assigned_without_copy(self):
        self.bug.visibility = "public"
        self.bug.save()
        count = Bug.objects.count()
        self.client.post(reverse("professor:assign", args=[self.group.pk]), {
            "bug": self.bug.pk, "title": "Own assignment",
        })
        self.assertEqual(Bug.objects.count(), count)
        self.assertEqual(self.group.assignments.get().bug_id, self.bug.pk)

    def test_copy_rolls_back_if_assignment_cannot_be_saved(self):
        count = Bug.objects.count()
        with patch("professor.views.Assignment.save", side_effect=IntegrityError("failed")):
            with self.assertRaises(IntegrityError):
                self.client.post(reverse("professor:assign", args=[self.group.pk]), {
                    "bug": self.public.pk, "title": "Failed assignment",
                })
        self.assertEqual(Bug.objects.count(), count)
        self.assertFalse(Assignment.objects.exists())

    def test_edit_form_omits_reference_solution_and_ignores_forged_changes(self):
        url = reverse("professor:bug", args=[self.bug.pk])
        page = self.client.get(url)
        self.assertNotContains(page, 'name="solution_code"')
        self.assertNotContains(page, self.bug.solution_code)
        response = self.client.post(url, {
            "title": "Updated title", "description": "Updated description",
            "difficulty": "easy", "revision": self.bug.revision,
            "solution_code": "forged reference",
        })
        self.assertRedirects(response, url)
        self.bug.refresh_from_db()
        self.assertEqual(self.bug.title, "Updated title")
        self.assertEqual(self.bug.solution_code, "return 1")

    def test_manual_creation_uses_language_choices_and_rejects_unknown_language(self):
        page = self.client.get(reverse("professor:create"))
        self.assertContains(page, '<select name="language"')
        data = self.exercise_data()
        data["language"] = "arbitrary-language"
        response = self.client.post(reverse("professor:create"), data)
        self.assertIn("language", response.context["form"].errors)
        self.assertFalse(Bug.objects.filter(title="Uploaded exercise").exists())

    def test_results_and_export_are_hidden_until_deadline_or_closure(self):
        for deadline in (None, timezone.now() + timedelta(days=1)):
            with self.subTest(deadline=deadline):
                assignment = self.assignment(deadline)
                Submission.objects.create(
                    assignment=assignment, bug=self.bug, student=self.student,
                    submitted_code="fixed", tests_passed=0, tests_total=5,
                )
                page = self.client.get(self.assignment_url("assignment", assignment))
                self.assertNotContains(page, self.student.email)
                self.assertEqual(self.client.get(
                    self.assignment_url("export", assignment),
                ).status_code, 403)
                self.client.post(self.assignment_url("close", assignment))
                page = self.client.get(self.assignment_url("assignment", assignment))
                self.assertContains(page, self.student.email)
                self.assertContains(page, "0 / 5")
                self.assertEqual(self.client.get(
                    self.assignment_url("export", assignment),
                ).status_code, 200)

    def test_best_verified_submission_and_csv_formula_protection(self):
        assignment = self.assignment(timezone.now() - timedelta(days=1))
        self.student.name = "=IMPORTXML(test)"
        self.student.save()
        for passed in (4, 1, None):
            Submission.objects.create(
                assignment=assignment, bug=self.bug, student=self.student,
                submitted_code="code", tests_passed=passed,
                tests_total=5 if passed is not None else None,
            )
        page = self.client.get(self.assignment_url("assignment", assignment))
        self.assertContains(page, "4 / 5")
        response = self.client.get(self.assignment_url("export", assignment))
        self.assertIn("'=IMPORTXML(test)", response.content.decode())
        self.assertIn(",4,5,Verified,Not checked", response.content.decode())
        self.assertNotIn("code", response.content.decode())
        self.assertEqual(response["Cache-Control"], "no-store")

    def test_other_teacher_cannot_read_results_or_change_assignment(self):
        assignment = self.assignment()
        self.client.force_login(self.other)
        for name in ("assignment", "close", "export"):
            url = self.assignment_url(name, assignment)
            response = self.client.post(url, {}) if name == "close" else self.client.get(url)
            self.assertEqual(response.status_code, 404)

    def ide_submit(self, assignment, payload):
        """Students submit from their VS Code (student.views.ide_submit), not a web form."""
        from student.models import IdeToken

        self.bug.project_files = {"main.py": self.bug.buggy_code, "test_main.py": "def test_x():\n    pass\n"}
        self.bug.entry_file = "main.py"
        self.bug.save()
        return self.client.post(
            reverse("student:ide_submit"), data=json.dumps(payload), content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {IdeToken.issue(self.student, self.bug, assignment)}",
        )

    def test_student_can_submit_without_deadline_until_manual_closure(self):
        assignment = self.assignment()
        self.client.force_login(self.student)
        url = reverse("student:assignment_workspace", args=[assignment.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        self.ide_submit(assignment, {"code": "fixed code"})
        self.assertEqual(assignment.submissions.count(), 1)
        assignment.status = "closed"
        assignment.save()
        self.ide_submit(assignment, {"code": "another fix"})
        self.assertEqual(assignment.submissions.count(), 1)

    def test_invalid_test_counts_are_rejected(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Submission.objects.create(
                student=self.student, bug=self.bug, submitted_code="code",
                tests_passed=6, tests_total=5,
            )

    @staticmethod
    def project_upload(files):
        stream = BytesIO()
        with ZipFile(stream, "w") as archive:
            for path, source in files.items():
                archive.writestr(path, source)
        return SimpleUploadedFile("project.zip", stream.getvalue(), "application/zip")

    def exercise_data(self):
        return {
            "title": "Uploaded exercise", "description": "Fix this",
            "language": "python", "difficulty": "easy", "solution_code": "fixed",
            "entry_file": "project/main.py",
            "project": self.project_upload({"project/main.py": "buggy", "project/test_main.py": "tests"}),
        }

    def test_creation_from_group_is_private_and_assigns_atomically(self):
        response = self.client.post(
            reverse("professor:create") + f"?group={self.group.pk}",
            self.exercise_data(),
        )
        self.assertRedirects(response, reverse("professor:group", args=[self.group.pk]))
        bug = Bug.objects.get(title="Uploaded exercise")
        self.assertEqual(bug.visibility, "private")
        self.assertEqual(bug.created_by, self.teacher)
        self.assertEqual(bug.project_files["project/main.py"], "buggy")
        self.assertEqual(self.group.assignments.get().bug, bug)

    def test_foreign_group_cannot_receive_created_exercise(self):
        response = self.client.post(
            reverse("professor:create") + f"?group={self.foreign_group.pk}",
            self.exercise_data(),
        )
        self.assertEqual(response.status_code, 404)
        self.assertFalse(Bug.objects.filter(title="Uploaded exercise").exists())

    def test_malformed_group_query_is_not_a_server_error(self):
        for pk in ("wrong", "0", "999999999999999999999999999"):
            self.assertEqual(self.client.get(
                reverse("professor:create"), {"group": pk},
            ).status_code, 404)

    def test_unsafe_project_paths_binary_and_secrets_are_rejected(self):
        for path, source in (("../escape.py", "x"), ("/absolute.py", "x"), (".env", "secret"), ("binary", b"\xff")):
            with self.subTest(path=path):
                data = self.exercise_data()
                data["project"] = self.project_upload({path: source})
                response = self.client.post(reverse("professor:create"), data)
                self.assertTrue(response.context["form"].errors)
        self.assertFalse(Bug.objects.filter(title="Uploaded exercise").exists())

    def test_missing_entry_file_keeps_invalid_project_unsaved(self):
        data = self.exercise_data()
        data["entry_file"] = "absent.py"
        response = self.client.post(reverse("professor:create"), data)
        self.assertIn("entry_file", response.context["form"].errors)
        self.assertFalse(Bug.objects.filter(title="Uploaded exercise").exists())

    def test_csrf_is_required_for_publication(self):
        from django.test import Client

        client = Client(enforce_csrf_checks=True)
        client.force_login(self.teacher)
        self.assertEqual(
            client.post(reverse("professor:publish", args=[self.bug.pk])).status_code, 403,
        )
        self.assertEqual(
            client.post(reverse("professor:unpublish", args=[self.bug.pk])).status_code, 403,
        )
        self.bug.refresh_from_db()
        self.assertEqual(self.bug.visibility, "private")

    def test_foreign_private_exercise_cannot_be_assigned_via_forged_form(self):
        response = self.client.post(reverse("professor:assign", args=[self.group.pk]), {
            "bug": self.foreign_bug.pk, "title": "Forged", "professor": self.other.pk,
        })
        self.assertTrue(response.context["form"].errors)
        self.assertFalse(Assignment.objects.exists())

    def test_fake_student_test_counts_are_not_saved(self):
        assignment = self.assignment()
        self.ide_submit(assignment, {"code": "fixed", "tests_passed": 999, "tests_total": 999})
        submission = assignment.submissions.get()
        self.assertEqual(submission.tests_passed, 1)
        self.assertEqual(submission.tests_total, 1)

    def test_no_deadline_and_closed_state_show_readable_student_page(self):
        assignment = self.assignment()
        self.client.force_login(self.student)
        url = reverse("student:assignment_detail", args=[assignment.pk])
        self.assertContains(self.client.get(url), "No deadline")
        assignment.status = "closed"
        assignment.save()
        self.assertContains(self.client.get(url), "This assignment is closed.")

    def test_empty_and_binary_archives_do_not_create_exercises(self):
        for project in (
            self.project_upload({}),
            SimpleUploadedFile("bad.zip", b"not a zip", "application/zip"),
        ):
            data = self.exercise_data()
            data["project"] = project
            response = self.client.post(reverse("professor:create"), data)
            self.assertIn("project", response.context["form"].errors)
        self.assertFalse(Bug.objects.filter(title="Uploaded exercise").exists())

    def test_compose_is_saved_per_exercise(self):
        data = self.exercise_data()
        data["compose_file"] = SimpleUploadedFile(
            "compose.yaml", b"services:\n  workspace:\n    image: python:3.12\n",
        )
        self.client.post(reverse("professor:create"), data)
        bug = Bug.objects.get(title="Uploaded exercise")
        self.assertIn("python:3.12", bug.compose_config)

    def test_legacy_shared_assignment_cannot_change_another_groups_deadline(self):
        assignment = self.assignment()
        second = StudyGroup.objects.create(name="Second group", professor=self.teacher)
        assignment.groups.add(second)
        response = self.client.post(self.assignment_url("assignment", assignment), {})
        self.assertContains(response, "shares a deadline across groups")
        self.client.post(self.assignment_url("close", assignment))
        assignment.refresh_from_db()
        self.assertEqual(assignment.status, "active")
