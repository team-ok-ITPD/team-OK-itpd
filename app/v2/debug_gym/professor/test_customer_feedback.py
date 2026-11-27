# [Professor Dev] Customer feedback regression checks
from importlib import import_module
from types import SimpleNamespace

from django.apps import apps
from django.db import connection
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

from core.models import Assignment, Bug, StudyGroup, Submission, User
from core.workspace_api import session_allowed
from professor.forms import ExerciseForm
from professor import tests as workflow


class CustomerFeedbackTests(TestCase):
    setUp = workflow.TeachingWorkflowTests.setUp
    assignment = workflow.TeachingWorkflowTests.assignment
    assignment_url = workflow.TeachingWorkflowTests.assignment_url
    exercise_data = workflow.TeachingWorkflowTests.exercise_data
    project_upload = staticmethod(workflow.TeachingWorkflowTests.project_upload)
    def test_private_filter_and_owner_names(self):
        page = self.client.get(reverse("professor:bugs"), {"scope": "private"})
        self.assertEqual(list(page.context["bugs"]), [self.bug])
        self.assertContains(page, f"Owner: {self.teacher.name}")
        self.assertContains(page, "hidden from other authors")
        self.assertContains(self.client.get(reverse("professor:bugs")), f"Owner: {self.other.name}")

    def test_admin_course_text_is_visible_but_teacher_cannot_edit_it(self):
        admin = User.objects.create_user("admin-feedback@test.local", "Admin", role="admin")
        self.client.force_login(admin)
        response = self.client.post(reverse("admin_panel:group-edit", args=[self.group.pk]), {
            "name": self.group.name, "group_number": "101", "course": "Algorithms <advanced>",
            "professor": self.teacher.pk, "description": "",
        })
        self.assertEqual(response.status_code, 302)
        self.client.force_login(self.teacher)
        url = reverse("professor:group", args=[self.group.pk])
        page = self.client.get(url)
        self.assertContains(page, "Algorithms &lt;advanced&gt;")
        self.assertNotContains(page, 'name="course"')
        self.client.post(url, {"course": "Forged"})
        self.group.refresh_from_db()
        self.assertEqual(self.group.course, "Algorithms <advanced>")

    def test_close_requires_explicit_confirmation_and_cancel_is_safe(self):
        assignment = self.assignment()
        url = self.assignment_url("close", assignment)
        for response in (self.client.get(url), self.client.post(url, {})):
            self.assertContains(response, "Close assignment?")
            self.assertContains(response, "Cancel")
            assignment.refresh_from_db()
            self.assertEqual(assignment.status, "active")
        self.client.post(url, {"confirm": "yes"})
        assignment.refresh_from_db()
        self.assertEqual(assignment.status, "closed")

    def test_unassign_archives_results_and_revokes_student_access(self):
        assignment = self.assignment()
        attempt = Submission.objects.create(
            assignment=assignment, bug=self.bug, student=self.student,
            submitted_code="submitted attempt", tests_passed=1, tests_total=2,
        )
        other = self.assignment(group=StudyGroup.objects.create(name="Other", professor=self.teacher))
        url = self.assignment_url("unassign", assignment)
        self.assertContains(self.client.get(url), "All submissions and results")
        self.client.post(url, {})
        assignment.refresh_from_db()
        self.assertFalse(assignment.is_withdrawn)
        self.client.post(url, {"confirm": "yes"})
        assignment.refresh_from_db()
        self.assertTrue(assignment.is_withdrawn)
        self.assertEqual(assignment.status, "closed")
        self.assertTrue(Submission.objects.filter(pk=attempt.pk).exists())
        self.assertTrue(Bug.objects.filter(pk=self.bug.pk).exists())
        self.assertContains(self.client.get(self.assignment_url("assignment", assignment)), self.student.email)
        self.assertEqual(self.client.get(self.assignment_url("export", assignment)).status_code, 200)
        other.refresh_from_db()
        self.assertEqual(other.status, "active")
        self.client.force_login(self.student)
        self.assertEqual(self.client.get(reverse("student:assignment_detail", args=[assignment.pk])).status_code, 404)
        self.assertFalse(session_allowed(SimpleNamespace(
            user=self.student, bug=self.bug, assignment_id=assignment.pk, assignment=assignment,
            authoring=False, expires_at=timezone.now()+timezone.timedelta(hours=1),
        )))
        self.client.force_login(self.other)
        self.assertEqual(self.client.post(url, {"confirm": "yes"}).status_code, 404)

    def test_minimum_upload_auto_detects_entry_and_has_no_reference_field(self):
        data = self.exercise_data()
        for field in ("entry_file", "description", "difficulty"):
            data.pop(field, None)
        page = self.client.get(reverse("professor:create"))
        self.assertContains(page, 'accept=".zip,application/zip"')
        self.assertNotIn("solution_code", ExerciseForm().fields)
        self.assertEqual(self.client.post(reverse("professor:create"), data).status_code, 302)
        bug = Bug.objects.get(title="Uploaded exercise")
        self.assertEqual(bug.entry_file, "project/main.py")
        self.assertEqual(bug.description, "")
        self.assertEqual(bug.difficulty, "easy")
        with connection.cursor() as cursor:
            columns = connection.introspection.get_table_description(cursor, "bugs")
        self.assertNotIn("solution_code", {column.name for column in columns})

    def test_upload_rejects_nonzip_extension_and_ambiguous_entry(self):
        for files, name in (({"main.py": "pass"}, "project.tar"),
                            ({"one.py": "pass", "two.py": "pass"}, "project.zip")):
            data = self.exercise_data()
            data["entry_file"] = ""
            data["project"] = self.project_upload(files)
            data["project"].name = name
            response = self.client.post(reverse("professor:create"), data)
            self.assertTrue(response.context["form"].errors)
        self.assertFalse(Bug.objects.filter(title="Uploaded exercise").exists())

    def test_upload_limits_remain_enforced_on_server(self):
        for files in ({f"file{i}.py": "pass" for i in range(101)}, {"main.py": "x"*5_000_001}):
            form = ExerciseForm({"title": "Too large", "language": "python"},
                                {"project": self.project_upload(files)})
            self.assertFalse(form.is_valid())
            self.assertIn("project", form.errors)

    def test_optional_dockerfile_rejects_yaml_binary_and_oversized_files(self):
        page = self.client.get(reverse("professor:create"))
        self.assertContains(page, 'name="dockerfile"')
        self.assertNotContains(page, 'name="compose_file"')
        for name, content in (("compose.yaml", b"services: {}"), ("Dockerfile", b"services: {}"),
                              ("Dockerfile", b"FROM python\n\xff"),
                              ("Dockerfile", b"FROM python\n"+b"x"*50_000)):
            data = self.exercise_data()
            data["dockerfile"] = SimpleUploadedFile(name, content)
            result = self.client.post(reverse("professor:create"), data)
            self.assertIn("dockerfile", result.context["form"].errors)
        self.assertFalse(Bug.objects.filter(title="Uploaded exercise").exists())

    def test_repeat_assignment_updates_only_this_group_deadline(self):
        first = self.assignment()
        group = StudyGroup.objects.create(name="Second", professor=self.teacher)
        second = self.assignment(group=group)
        due = (timezone.now()+timezone.timedelta(days=4)).strftime("%Y-%m-%dT%H:%M")
        self.client.post(reverse("professor:assign", args=[self.group.pk]), {
            "bug": self.bug.pk, "title": "Updated", "deadline": due,
        })
        first.refresh_from_db()
        second.refresh_from_db()
        self.assertEqual(Assignment.objects.count(), 2)
        self.assertIsNotNone(first.deadline)
        self.assertIsNone(second.deadline)

    def test_legacy_multigroup_split_preserves_attempts_and_independent_deadlines(self):
        assignment = self.assignment()
        second = StudyGroup.objects.create(name="Legacy second", professor=self.teacher)
        second.students.add(self.student)
        assignment.groups.add(second)
        Submission.objects.create(assignment=assignment, bug=self.bug, student=self.student, submitted_code="old")
        migration = import_module("core.migrations.0007_teaching_customer_feedback")
        migration.separate_groups(apps, SimpleNamespace(connection=connection))
        copy = second.assignments.get()
        self.assertNotEqual(copy.pk, assignment.pk)
        self.assertEqual(copy.submissions.get().submitted_code, "old")
        due = (timezone.now()+timezone.timedelta(days=2)).strftime("%Y-%m-%dT%H:%M")
        self.client.post(self.assignment_url("assignment", assignment), {"deadline": due})
        copy.refresh_from_db()
        self.assertIsNone(copy.deadline)

    def test_legacy_duplicate_pair_is_archived_without_deleting_attempts(self):
        old = self.assignment()
        current = self.assignment()
        attempt = Submission.objects.create(assignment=old, bug=self.bug, student=self.student, submitted_code="old")
        migration = import_module("core.migrations.0007_teaching_customer_feedback")
        migration.separate_groups(apps, SimpleNamespace(connection=connection))
        old.refresh_from_db()
        current.refresh_from_db()
        self.assertTrue(old.is_withdrawn)
        self.assertFalse(current.is_withdrawn)
        self.assertTrue(Submission.objects.filter(pk=attempt.pk).exists())
