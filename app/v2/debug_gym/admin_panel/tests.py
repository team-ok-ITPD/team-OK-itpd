# [Admin Dev] Meeting-feedback regression tests for accounts, import and memberships
import io
import re

from django.core import mail
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from core.models import Bug, GroupStudent, StudyGroup, Submission, User

from .imports import import_students


class AdminPanelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user(
            "admin@example.com", "Admin", "debug-gym-pass", role=User.Role.ADMIN
        )
        cls.teacher = User.objects.create_user(
            "teacher@example.com", "Teacher", "debug-gym-pass", role=User.Role.PROFESSOR
        )
        cls.student = User.objects.create_user(
            "student@example.com", "Student", "debug-gym-pass"
        )
        cls.group = StudyGroup.objects.create(
            name="Python A", description="Programming", professor=cls.teacher
        )

    def setUp(self):
        self.client.force_login(self.admin)

    def payload(self, **overrides):
        data = {
            "name": "New account", "email": "new@example.com", "is_active": "on",
            "password": "new-password",
        }
        data.update(overrides)
        return data

    def batch(self, action, students=None, group=None):
        return self.client.post(reverse("admin_panel:student-batch"), {
            "action": action,
            "students": students if students is not None else [self.student.pk],
            "group": group if group is not None else self.group.pk,
        })

    def upload(self, csv):
        return self.client.post(reverse("admin_panel:student-import"), {
            "file": SimpleUploadedFile("students.csv", csv.encode("utf-8")),
            "confirm": "on",
        })

    def test_create_roles_hashes_password_and_ignores_role_injection(self):
        for route, role, destination in (
            ("user-create", User.Role.PROFESSOR, "users"),
            ("student-create", User.Role.STUDENT, "students"),
            ("administrator-create", User.Role.ADMIN, "administrators"),
        ):
            with self.subTest(role=role):
                response = self.client.post(reverse(f"admin_panel:{route}"), self.payload(
                    email=f"{role}-new@example.com", role="professor"
                ))
                self.assertRedirects(response, reverse(f"admin_panel:{destination}"))
                account = User.objects.get(email=f"{role}-new@example.com")
                self.assertEqual(account.role, role)
                self.assertFalse(account.has_usable_password())
                self.assertNotEqual(account.password, "new-password")

    def test_account_validation_and_single_password_field(self):
        for route in ("user-create", "student-create", "administrator-create"):
            response = self.client.get(reverse(f"admin_panel:{route}"))
            self.assertNotContains(response, 'name="password"')
            self.assertNotIn("password", response.context["form"].fields)
            self.assertNotContains(response, 'name="password_confirmation"')
            for invalid in (
                {"email": "invalid"}, {"email": self.teacher.email.upper()},
            ):
                with self.subTest(route=route, invalid=invalid):
                    response = self.client.post(
                        reverse(f"admin_panel:{route}"), self.payload(**invalid)
                    )
                    self.assertEqual(response.status_code, 200)
                    self.assertTrue(response.context["form"].errors)
                    self.assertNotContains(response, f'value="{invalid.get("password", "not-submitted")}"')

    def test_account_actions_share_toolbar_without_nested_forms_or_saved_password(self):
        response = self.client.get(
            reverse("admin_panel:user-edit", args=[self.teacher.pk])
        )
        self.assertContains(response, 'form="account-access-link-form"')
        self.assertContains(response, 'id="account-access-link-form"')
        self.assertContains(response, "Delete account")
        self.assertContains(response, 'class="button secondary admin-account-cancel"')
        self.assertNotContains(response, 'name="password"')
        self.assertLess(
            response.content.index(b">Delete account<"),
            response.content.index(b">Cancel<"),
        )
        self.assertNotContains(response, self.teacher.password)
        self.assertNotContains(response, 'value="debug-gym-pass"')

    def test_edit_all_roles_retains_role_and_blank_password(self):
        for route, account, destination in (
            ("user-edit", self.teacher, "users"),
            ("student-edit", self.student, "students"),
            ("administrator-edit", self.admin, "administrators"),
        ):
            with self.subTest(route=route):
                response = self.client.post(
                    reverse(f"admin_panel:{route}", args=[account.pk]),
                    self.payload(name="Updated", email=account.email, password="", role="student"),
                )
                self.assertRedirects(response, reverse(f"admin_panel:{destination}"))
                original_role = account.role
                account.refresh_from_db()
                self.assertEqual(account.name, "Updated")
                self.assertEqual(account.role, original_role)
                self.assertTrue(account.check_password("debug-gym-pass"))

    def test_edit_ignores_injected_password_and_preserves_self_session(self):
        response = self.client.post(
            reverse("admin_panel:administrator-edit", args=[self.admin.pk]),
            self.payload(email=self.admin.email),
        )
        self.assertRedirects(response, reverse("admin_panel:administrators"))
        self.admin.refresh_from_db()
        self.assertTrue(self.admin.check_password("debug-gym-pass"))
        self.assertEqual(self.client.get(reverse("admin_panel:dashboard")).status_code, 200)

    def test_self_deactivation_and_cross_role_edit_refused(self):
        self.assertEqual(self.client.get(reverse(
            "admin_panel:student-edit", args=[self.admin.pk]
        )).status_code, 404)
        data = self.payload(email=self.admin.email, password="")
        del data["is_active"]
        response = self.client.post(reverse(
            "admin_panel:administrator-edit", args=[self.admin.pk]
        ), data)
        self.assertContains(response, "You cannot deactivate your own")
        self.admin.refresh_from_db()
        self.assertTrue(self.admin.is_active)

    def test_management_pages_render_without_assignments_or_group_members_page(self):
        for route in (
            "dashboard", "users", "students", "administrators", "groups", "group-create",
            "student-create", "administrator-create", "student-import",
        ):
            response = self.client.get(reverse(f"admin_panel:{route}"))
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, "/admin-panel/assignments/")
        for old in (
            "/admin-panel/assignments/", "/admin-panel/assignments/1/",
            f"/admin-panel/groups/{self.group.pk}/",
            f"/admin-panel/groups/{self.group.pk}/members/",
        ):
            self.assertEqual(self.client.get(old).status_code, 404)
        groups = self.client.get(reverse("admin_panel:groups"))
        self.assertNotContains(groups, "Manage members")
        self.assertContains(groups, "Edit group")
        group_url = reverse("admin_panel:group-edit", args=[self.group.pk])
        self.assertContains(groups, f'data-row-link="{group_url}"')
        students = self.client.get(reverse("admin_panel:students"))
        self.assertContains(students, 'aria-label="Student filters and bulk actions"')
        self.assertContains(students, 'class="admin-toolbar-filters"')
        self.assertContains(students, 'class="admin-toolbar-batch"')
        self.assertNotContains(students, '<h2 class="card-title">Bulk actions</h2>')

    def test_all_management_routes_are_admin_only(self):
        urls = [reverse(f"admin_panel:{route}") for route in (
            "dashboard", "users", "students", "administrators", "groups", "group-create",
            "user-create", "student-create", "administrator-create", "student-import",
            "student-batch",
        )] + [
            reverse("admin_panel:group-edit", args=[self.group.pk]),
            reverse("admin_panel:student-edit", args=[self.student.pk]),
            reverse("admin_panel:administrator-edit", args=[self.admin.pk]),
            reverse("admin_panel:account-delete", args=[self.student.pk]),
            reverse("admin_panel:account-access-link", args=[self.student.pk]),
        ]
        for account in (None, self.student, self.teacher):
            self.client.logout()
            if account:
                self.client.force_login(account)
            for url in urls:
                for method in ("get", "post"):
                    with self.subTest(account=account, url=url, method=method):
                        self.assertEqual(
                            getattr(self.client, method)(url).status_code, 403 if account else 302
                        )

    def test_group_create_edit_teacher_validation_search_and_navigation(self):
        response = self.client.post(reverse("admin_panel:group-create"), {
            "name": "New group", "description": "Software Development\nLab group",
            "group_number": "01", "professor": self.teacher.pk,
        })
        self.assertRedirects(response, reverse("admin_panel:groups"))
        group = StudyGroup.objects.get(name="New group")
        self.assertEqual(group.group_number, "")
        form_url = reverse("admin_panel:group-edit", args=[group.pk])
        response = self.client.get(form_url)
        self.assertContains(response, "data-searchable-select")
        self.assertIsNone(response.context["form"].fields["professor"].empty_label)
        self.assertNotContains(response, '<option value="">')
        response = self.client.post(form_url, {
            "name": group.name, "group_number": "01", "professor": "",
        })
        self.assertIn("professor", response.context["form"].errors)
        for account in (self.student, self.admin):
            response = self.client.post(form_url, {
                "name": "Changed", "group_number": "01", "description": "Course",
                "professor": account.pk,
            })
            self.assertTrue(response.context["form"].errors)
        response = self.client.get(reverse("admin_panel:groups"), {"q": "Software"})
        self.assertContains(response, "New group")
        self.teacher.is_active = False
        self.teacher.save()
        response = self.client.post(form_url, {
            "name": group.name, "group_number": "01", "professor": self.teacher.pk,
        })
        self.assertRedirects(response, reverse("admin_panel:groups"))

    def test_group_name_replaces_separate_number_and_legacy_identity_survives(self):
        url = reverse("admin_panel:group-create")
        response = self.client.get(url)
        self.assertContains(response, 'name="course"')
        self.assertNotContains(response, 'name="group_number"')
        response = self.client.post(url, {
            "name": "Programming A", "course": "Programming",
            "professor": self.teacher.pk, "is_active": "on",
        })
        self.assertRedirects(response, reverse("admin_panel:groups"))
        self.assertEqual(StudyGroup.objects.get(name="Programming A").group_number, "")
        for number in ("001", "BS-23"):
            group = StudyGroup.objects.create(
                name="Programming", group_number=number, professor=self.teacher,
            )
            self.assertEqual(str(group), "Programming")
            group.students.add(self.student)
        response = self.client.get(reverse("admin_panel:groups"), {"q": "BS-23"})
        self.assertContains(response, "Programming")
        # The search input echoes the query; group labels must omit the number.
        self.assertNotContains(response, "Programming · BS-23")
        self.assertNotContains(response, "Programming · 001")
        response = self.client.get(reverse("admin_panel:students"))
        self.assertContains(response, "Programming")
        self.assertNotContains(response, "Programming · 001")
        self.assertNotContains(response, "Programming · BS-23")
        for user, route in ((self.student, "student:dashboard"), (self.teacher, "professor:dashboard")):
            client = Client()
            client.force_login(user)
            response = client.get(reverse(route))
            self.assertContains(response, "Programming")
            self.assertNotContains(response, "Programming · 001")
            self.assertNotContains(response, "Programming · BS-23")

    def test_duplicate_course_number_rejected_and_legacy_numbers_not_invented(self):
        from django.db import IntegrityError, transaction

        self.assertEqual(self.group.group_number, "")
        self.assertEqual(str(self.group), self.group.name)
        StudyGroup.objects.create(
            name="Programming", group_number="01", professor=self.teacher,
        )
        response = self.client.post(reverse("admin_panel:group-create"), {
            "name": "programming", "group_number": "01", "professor": self.teacher.pk,
        })
        self.assertIn("name", response.context["form"].errors)
        with self.assertRaises(IntegrityError), transaction.atomic():
            StudyGroup.objects.create(
                name="PROGRAMMING", group_number="01", professor=self.teacher,
            )

    def test_student_filter_search_counter_and_pagination(self):
        self.group.students.add(self.student)
        User.objects.bulk_create([
            User(email=f"student{i}@example.com", name=f"Learner {i:02}") for i in range(31)
        ])
        url = reverse("admin_panel:students")
        response = self.client.get(url, {"group": self.group.pk, "q": "STUDENT@"})
        self.assertEqual(response.context["student_total"], 1)
        self.assertNotContains(response, "students match.")
        self.assertNotContains(response, 'aria-label="1 students"')
        self.assertContains(response, self.student.email)
        self.assertContains(response, self.teacher.name)
        response = self.client.get(url)
        self.assertEqual(len(response.context["accounts"]), 30)
        self.assertContains(response, "?page=2")
        self.assertEqual(len(self.client.get(url, {"page": 2}).context["accounts"]), 2)
        self.assertEqual(self.client.get(url, {"q": "missing"}).context["student_total"], 0)
        for invalid_group in ("not-a-number", "9" * 5000):
            self.assertEqual(self.client.get(
                url, {"group": invalid_group}
            ).context["student_total"], 0)

    def test_student_count_includes_second_page_and_bulk_action_accepts_it(self):
        User.objects.bulk_create([
            User(email=f"pagination{i:02}@example.com", name=f"Pagination {i:02}")
            for i in range(1, 45)
        ])
        url = reverse("admin_panel:students")
        first = self.client.get(url)
        second = self.client.get(url, {"page": 2})
        self.assertEqual(first.context["student_total"], 45)
        self.assertEqual(second.context["student_total"], 45)
        self.assertEqual(len(first.context["accounts"]), 30)
        self.assertEqual(len(second.context["accounts"]), 15)
        selected = [first.context["accounts"][0].pk, list(second.context["accounts"])[-1].pk]
        self.assertEqual(self.batch("deactivate", students=selected).status_code, 302)
        self.assertEqual(User.objects.filter(pk__in=selected, is_active=False).count(), 2)
        self.assertEqual(User.objects.filter(role=User.Role.STUDENT, is_active=False).count(), 2)

    def test_batch_add_repeat_remove_preserves_submissions(self):
        bug = Bug.objects.create(
            title="Example", description="Fix", buggy_code="pass",
            language="python", created_by=self.teacher,
        )
        submission = Submission.objects.create(
            student=self.student, bug=bug, submitted_code="fixed"
        )
        for _ in range(2):
            self.assertRedirects(self.batch("add"), reverse("admin_panel:students"))
        self.assertEqual(GroupStudent.objects.count(), 1)
        self.assertEqual(self.batch("remove").status_code, 302)
        self.assertEqual(GroupStudent.objects.count(), 0)
        self.assertTrue(Submission.objects.filter(pk=submission.pk).exists())

    def test_batch_preserves_explicit_list_filters(self):
        response = self.client.post(reverse("admin_panel:student-batch"), {
            "action": "add", "students": [self.student.pk], "group": self.group.pk,
            "filter_q": "Student & name", "filter_group": self.group.pk, "filter_page": "2",
        })
        self.assertEqual(
            response.url,
            reverse("admin_panel:students")
            + f"?q=Student+%26+name&group={self.group.pk}&page=2",
        )

    def test_status_actions_ignore_groups_and_preserve_memberships(self):
        self.group.students.add(self.student)
        for action, active in (("deactivate", False), ("activate", True)):
            for group in (str(self.group.pk), "invalid", ""):
                response = self.batch(action, group=group)
                self.assertRedirects(response, reverse("admin_panel:students"))
                self.student.refresh_from_db()
                self.assertEqual(self.student.is_active, active)
                self.assertTrue(self.group.students.filter(pk=self.student.pk).exists())

    def test_batch_target_group_starts_empty_without_dash_label(self):
        response = self.client.get(reverse("admin_panel:students"))
        choices = list(response.context["batch_form"].fields["group"].choices)
        self.assertTrue(choices)
        self.assertEqual(choices[0], ("", ""))
        self.assertIsNone(response.context["batch_form"]["group"].value())
        filtered = self.client.get(reverse("admin_panel:students"), {"group": self.group.pk})
        self.assertIsNone(filtered.context["batch_form"]["group"].value())
        response = self.batch("add")
        self.assertRedirects(response, reverse("admin_panel:students"))
        response = self.client.get(response.url)
        self.assertIsNone(response.context["batch_form"]["group"].value())

    def test_batch_selection_reset_only_after_success(self):
        self.assertEqual(self.batch("add", group="").status_code, 400)
        response = self.client.get(reverse("admin_panel:students"))
        self.assertFalse(response.context["reset_student_selection"])
        response = self.batch("activate")
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertTrue(response.context["reset_student_selection"])
        response = self.client.get(reverse("admin_panel:students"))
        self.assertFalse(response.context["reset_student_selection"])

    def test_batch_rejects_wrong_role_empty_selection_and_missing_group(self):
        for students in ([], [self.admin.pk], [self.teacher.pk], [99999]):
            self.assertEqual(self.batch("add", students=students).status_code, 400)
        self.assertEqual(self.batch("add", group="").status_code, 400)
        self.assertEqual(GroupStudent.objects.count(), 0)

    def test_deactivation_keeps_student_group_and_assignment_access_and_sorts_last(self):
        from core.models import Assignment
        from django.utils import timezone
        from datetime import timedelta

        self.group.students.add(self.student)
        bug = Bug.objects.create(
            title="Historical material", description="Keep access", created_by=self.teacher,
        )
        assignment = Assignment.objects.create(
            title="Historical assignment", professor=self.teacher,
            bug=bug, deadline=timezone.now() + timedelta(days=2),
        )
        assignment.groups.add(self.group)
        active = StudyGroup.objects.create(name="Z active", professor=self.teacher)
        response = self.client.post(reverse("admin_panel:group-edit", args=[self.group.pk]), {
            "name": self.group.name, "course": "Programming", "professor": self.teacher.pk,
        })
        self.assertEqual(response.status_code, 302)
        self.group.refresh_from_db()
        self.assertFalse(self.group.is_active)
        self.assertTrue(self.group.students.filter(pk=self.student.pk).exists())
        self.assertTrue(Assignment.objects.filter(pk=assignment.pk).exists())
        response = self.client.get(reverse("admin_panel:groups"))
        self.assertEqual(list(response.context["groups"]), [active, self.group])
        student = Client()
        student.force_login(self.student)
        response = student.get(reverse("student:dashboard"))
        self.assertContains(response, self.group.name)
        response = student.get(reverse("student:assignment_detail", args=[assignment.pk]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("admin_panel:group-edit", args=[self.group.pk]), {
            "name": self.group.name, "professor": self.teacher.pk, "is_active": "on",
        })
        self.assertEqual(response.status_code, 302)
        self.group.refresh_from_db()
        self.assertTrue(self.group.is_active)

    def test_edit_inactive_student_multiple_memberships_without_activation(self):
        other = StudyGroup.objects.create(name="Other", professor=self.teacher, is_active=False)
        self.student.is_active = False
        self.student.save()
        url = reverse("admin_panel:student-edit", args=[self.student.pk])
        data = self.payload(
            email=self.student.email, name=self.student.name, password="",
            groups=[self.group.pk, other.pk],
        )
        data.pop("is_active")
        self.assertEqual(self.client.post(url, data).status_code, 302)
        self.assertSetEqual(set(self.student.study_groups.all()), {self.group, other})
        self.student.refresh_from_db()
        self.assertFalse(self.student.is_active)
        data["groups"] = [other.pk]
        self.assertEqual(self.client.post(url, data).status_code, 302)
        self.assertEqual(list(self.student.study_groups.all()), [other])

    def test_batch_activity_revokes_existing_web_session(self):
        student_client = Client()
        student_client.force_login(self.student)
        idle_client = Client()
        idle_client.force_login(self.student)
        self.assertEqual(self.batch("deactivate").status_code, 302)
        self.assertEqual(student_client.get(reverse("student:dashboard")).status_code, 302)
        self.assertEqual(self.batch("add").status_code, 302)
        self.student.refresh_from_db()
        self.assertFalse(self.student.is_active)
        self.assertEqual(self.batch("remove").status_code, 302)
        self.assertEqual(self.batch("activate").status_code, 302)
        self.assertEqual(idle_client.get(reverse("student:dashboard")).status_code, 302)
        self.assertEqual(self.batch("add").status_code, 302)

    def test_deactivation_revokes_ide_tokens_on_edit_and_csv(self):
        from student.models import IdeToken

        bug = Bug.objects.create(
            title="Example", description="Fix", buggy_code="pass",
            language="python", created_by=self.teacher,
        )
        token = IdeToken.issue(self.student, bug)
        self.client.post(
            reverse("admin_panel:student-edit", args=[self.student.pk]),
            {"name": self.student.name, "email": self.student.email, "password": ""},
        )
        self.assertIsNone(IdeToken.find(token))
        self.student.is_active = True
        self.student.save()
        token = IdeToken.issue(self.student, bug)
        self.assertEqual(self.upload(
            "name,email,is_active\nStudent,student@example.com,false\n"
        ).status_code, 302)
        self.assertIsNone(IdeToken.find(token))

    def test_mutations_need_post_and_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.admin)
        urls = [
            reverse("admin_panel:student-batch"),
            reverse("admin_panel:account-access-link", args=[self.student.pk]),
        ]
        for url in urls:
            self.assertEqual(self.client.get(url).status_code, 405)
        urls += [
            reverse("admin_panel:student-import"),
            reverse("admin_panel:account-delete", args=[self.student.pk]),
        ]
        for url in urls:
            self.assertEqual(client.post(url, {}).status_code, 403)

    def test_csv_create_group_students_and_repeat_is_idempotent(self):
        csv = (
            "name,email,is_active,password,group,teacher_email,course,group_number\n"
            "First,first@example.com,true,new-password,New group,teacher@example.com,Python,01\n"
            "First,first@example.com,true,new-password,Python A,,,\n"
            "Second,second@example.com,false,new-password,,,,\n"
        )
        self.assertRedirects(self.upload(csv), reverse("admin_panel:students"))
        student = User.objects.get(email="first@example.com")
        old_hash = student.password
        self.assertEqual(student.study_groups.count(), 2)
        self.assertFalse(student.has_usable_password())
        self.assertFalse(User.objects.get(email="second@example.com").is_active)
        self.assertRedirects(self.upload(csv), reverse("admin_panel:students"))
        student.refresh_from_db()
        self.assertEqual(student.password, old_hash)
        self.assertEqual(student.study_groups.count(), 2)
        self.assertEqual(StudyGroup.objects.filter(name="New group").count(), 1)

    def test_csv_updates_existing_and_blank_fields_preserve_password_status_groups(self):
        self.group.students.add(self.student)
        original_hash = self.student.password
        response = self.upload("name,email,is_active,password\nUpdated,STUDENT@example.com,,\n")
        self.assertEqual(response.status_code, 302)
        self.student.refresh_from_db()
        self.assertEqual(self.student.name, "Updated")
        self.assertEqual(self.student.password, original_hash)
        self.assertTrue(self.student.is_active)
        self.assertTrue(self.student.study_groups.filter(pk=self.group.pk).exists())

    def test_csv_distinguishes_group_numbers_within_one_course(self):
        csv = (
            "name,email,password,course,group_number,teacher_email\n"
            "Multi,multi@example.com,new-password,Programming,001,teacher@example.com\n"
            "Multi,multi@example.com,new-password,Programming,BS-23,teacher@example.com\n"
        )
        for _ in range(2):
            self.assertEqual(self.upload(csv).status_code, 302)
        student = User.objects.get(email="multi@example.com")
        self.assertEqual(student.study_groups.count(), 2)
        self.assertEqual(StudyGroup.objects.filter(name="Programming").count(), 2)
        response = self.upload("name,email,course\nMulti,multi@example.com,Programming\n")
        self.assertContains(response, "supply group_number", status_code=400)
        self.assertEqual(self.upload(
            "name,email,course,group_number\nMulti,multi@example.com,programming,BS-23\n"
        ).status_code, 302)
        self.assertEqual(student.study_groups.count(), 2)
        self.assertEqual(StudyGroup.objects.filter(name="Programming").count(), 2)

    def test_csv_errors_roll_back_all_rows_and_dont_echo_passwords(self):
        cases = (
            "Other,teacher@example.com,new-password,,,\n",
            "Other,invalid,new-password,,,\n",
            "Other,other@example.com,new-password,G,missing@example.com,Course\n",
            "Other,other@example.com,new-password,Python A,admin@example.com,Programming\n",
            "Other,other@example.com,new-password,,,\nDifferent,other@example.com,new-password,,,\n",
        )
        for invalid in cases:
            with self.subTest(invalid=invalid):
                csv = ("name,email,password,group,teacher_email,course\n"
                       "Valid,valid@example.com,new-password,,,\n" + invalid)
                response = self.upload(csv)
                self.assertEqual(response.status_code, 400)
                self.assertFalse(User.objects.filter(email="valid@example.com").exists())
                self.assertNotContains(response, "new-password", status_code=400)

    def test_csv_schema_encoding_limits_and_ambiguity(self):
        for csv in (
            "name,email,email\nX,x@example.com,x@example.com\n",
            "name,email,role\nX,x@example.com,admin\n",
            "name,email\n",
            "name,email,password\nX,x@example.com\n",
        ):
            with self.assertRaises(ValidationError):
                import_students(io.BytesIO(csv.encode()))
        with self.assertRaises(ValidationError):
            import_students(io.BytesIO(b"\xff"))
        with self.assertRaises(ValidationError):
            import_students(io.BytesIO(b"x" * 1_000_001))
        StudyGroup.objects.create(name=self.group.name, professor=self.teacher)
        self.assertEqual(self.upload(
            "name,email,password,group\nX,x@example.com,new-password,Python A\n"
        ).status_code, 400)
        self.assertFalse(User.objects.filter(email="x@example.com").exists())

    def test_failed_csv_rolls_back_session_revocation(self):
        student_client = Client()
        student_client.force_login(self.student)
        response = self.upload(
            "name,email,is_active\nStudent,student@example.com,false\n"
            "Teacher,teacher@example.com,false\n"
        )
        self.assertEqual(response.status_code, 400)
        self.student.refresh_from_db()
        self.assertTrue(self.student.is_active)
        self.assertEqual(student_client.get(reverse("student:dashboard")).status_code, 200)

    def test_changing_group_teacher_preserves_assignments_and_members(self):
        from core.models import Assignment

        other = User.objects.create_user("other@example.com", "Other", role=User.Role.PROFESSOR)
        bug = Bug.objects.create(
            title="Example", description="Fix", buggy_code="pass",
            language="python", created_by=self.teacher,
        )
        assignment = Assignment.objects.create(title="Example", bug=bug, professor=self.teacher)
        assignment.groups.add(self.group)
        self.group.students.add(self.student)
        response = self.client.post(
            reverse("admin_panel:group-edit", args=[self.group.pk]),
            {"name": self.group.name, "group_number": "01",
             "description": "Programming", "professor": other.pk},
        )
        self.assertRedirects(response, reverse("admin_panel:groups"))
        self.group.refresh_from_db()
        assignment.refresh_from_db()
        bug.refresh_from_db()
        self.assertEqual(self.group.professor, other)
        self.assertEqual(assignment.professor, self.teacher)
        self.assertEqual(bug.created_by, self.teacher)
        self.assertTrue(self.group.students.filter(pk=self.student.pk).exists())

    def test_delete_requires_explicit_confirmation_and_blocks_self(self):
        url = reverse("admin_panel:account-delete", args=[self.student.pk])
        self.assertContains(self.client.get(url), "Permanently delete account")
        self.assertTrue(User.objects.filter(pk=self.student.pk).exists())
        self.assertEqual(self.client.post(url).status_code, 400)
        self.assertRedirects(self.client.post(url, {"confirm": "yes"}), reverse("admin_panel:students"))
        self.assertFalse(User.objects.filter(pk=self.student.pk).exists())
        self.assertEqual(self.client.post(
            reverse("admin_panel:account-delete", args=[self.admin.pk]), {"confirm": "yes"}
        ).status_code, 400)
        self.assertTrue(User.objects.filter(pk=self.admin.pk).exists())

    def test_delete_protects_teacher_and_student_history(self):
        bug = Bug.objects.create(
            title="Example", description="Fix", buggy_code="pass",
            language="python", created_by=self.teacher,
        )
        Submission.objects.create(student=self.student, bug=bug, submitted_code="fixed")
        for account in (self.teacher, self.student):
            self.assertEqual(self.client.post(
                reverse("admin_panel:account-delete", args=[account.pk]), {"confirm": "yes"}
            ).status_code, 400)
            self.assertTrue(User.objects.filter(pk=account.pk).exists())
        other = User.objects.create_user("other@example.com", "Other", role=User.Role.ADMIN)
        self.assertRedirects(self.client.post(
            reverse("admin_panel:account-delete", args=[other.pk]), {"confirm": "yes"}
        ), reverse("admin_panel:administrators"))

    @override_settings(
        ACCOUNT_EMAIL_ENABLED=True, ACCOUNT_PUBLIC_URL="http://testserver",
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    )
    def test_creation_emails_initial_password_for_every_account_role(self):
        password = "initial-notification-password"
        for index, (route, role) in enumerate((
            ("student-create", User.Role.STUDENT),
            ("user-create", User.Role.PROFESSOR),
            ("administrator-create", User.Role.ADMIN),
        ), 1):
            with self.subTest(role=role):
                email = f"initial-{role}@example.com"
                response = self.client.post(
                    reverse(f"admin_panel:{route}"),
                    self.payload(email=email, password=password),
                    follow=True,
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(mail.outbox), index)
                message = mail.outbox[-1]
                self.assertEqual(message.to, [email])
                self.assertEqual(message.subject, "Welcome to Debug Gym — your account is ready")
                self.assertIn("Welcome to Debug Gym!", message.body)
                self.assertIn("Role:", message.body)
                self.assertIn("Keep this email private", message.body)
                self.assertNotIn(password, message.body)
                self.assertIn(f"http://testserver{reverse('accounts:login')}", message.body)
                self.assertIn("/accounts/set-password/", message.body)
                user = User.objects.get(email=email)
                self.assertEqual(user.role, role)
                self.assertNotEqual(user.password, password)
                self.assertFalse(user.has_usable_password())
                self.assertNotIn(user.password, message.body)
                self.assertFalse(Client().login(email=email, password=password))
                self.assertNotContains(response, password)

    @override_settings(
        ACCOUNT_EMAIL_ENABLED=True, ACCOUNT_PUBLIC_URL="http://testserver",
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    )
    def test_creation_does_not_email_inactive_or_invalid_accounts(self):
        data = self.payload()
        del data["is_active"]
        self.assertEqual(self.client.post(
            reverse("admin_panel:student-create"), data
        ).status_code, 302)
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(self.client.post(
            reverse("admin_panel:user-create"), self.payload(email="invalid-email")
        ).status_code, 200)
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(
        ACCOUNT_EMAIL_ENABLED=False, ACCOUNT_PUBLIC_URL="http://testserver",
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    )
    def test_creation_keeps_password_but_sends_nothing_when_email_is_disabled(self):
        self.assertEqual(self.client.post(
            reverse("admin_panel:student-create"), self.payload()
        ).status_code, 302)
        self.assertEqual(len(mail.outbox), 0)
        self.assertFalse(User.objects.get(email="new@example.com").has_usable_password())

    @override_settings(
        ACCOUNT_EMAIL_ENABLED=True, ACCOUNT_PUBLIC_URL="http://testserver",
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    )
    def test_creation_delivery_failure_does_not_leak_password_or_undo_account(self):
        from unittest.mock import patch

        password = "private-initial-password"
        with patch("admin_panel.mail.send_mail", side_effect=RuntimeError(password)):
            response = self.client.post(
                reverse("admin_panel:student-create"),
                self.payload(password=password), follow=True,
            )
        self.assertContains(response, "Access email was not sent")
        self.assertNotContains(response, password)
        self.assertFalse(User.objects.get(email="new@example.com").has_usable_password())
        self.assertEqual(len(mail.outbox), 0)

    @override_settings(
        ACCOUNT_EMAIL_ENABLED=True, ACCOUNT_PUBLIC_URL="http://testserver",
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    )
    def test_manual_resend_never_recovers_or_resends_initial_password(self):
        password = "initial-notification-password"
        self.client.post(
            reverse("admin_panel:student-create"), self.payload(password=password)
        )
        user = User.objects.get(email="new@example.com")
        response = self.client.post(reverse(
            "admin_panel:account-access-link", args=[user.pk]
        ), follow=True)
        self.assertEqual(len(mail.outbox), 2)
        self.assertNotIn(password, mail.outbox[0].body)
        self.assertNotIn(password, mail.outbox[1].body)
        self.assertNotIn("Initial password:", mail.outbox[1].body)
        self.assertEqual(mail.outbox[1].subject, "Debug Gym — your password setup link")
        self.assertIn("Opening this email alone does not change your password", mail.outbox[1].body)
        self.assertContains(response, "No password was sent.")

    @override_settings(
        ACCOUNT_EMAIL_ENABLED=True, ACCOUNT_PUBLIC_URL="http://testserver",
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    )
    def test_csv_creation_emails_initial_password_only_once(self):
        csv = (
            "name,email,password,group,teacher_email,course,group_number\n"
            "Imported,imported@example.com,initial-csv-password,Python A,,,\n"
            "Imported,imported@example.com,initial-csv-password,Second group,teacher@example.com,Python,01\n"
        )
        self.assertEqual(self.upload(csv).status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertNotIn("initial-csv-password", mail.outbox[0].body)
        self.assertEqual(self.upload(csv).status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        user = User.objects.get(email="imported@example.com")
        self.assertFalse(user.has_usable_password())
        self.assertEqual(user.study_groups.count(), 2)

    @override_settings(
        ACCOUNT_EMAIL_ENABLED=True, ACCOUNT_PUBLIC_URL="http://testserver",
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    )
    def test_access_email_has_one_time_link_not_password(self):
        response = self.client.post(reverse("admin_panel:student-create"), self.payload(password=""))
        self.assertRedirects(response, reverse("admin_panel:students"))
        user = User.objects.get(email="new@example.com")
        self.assertFalse(user.has_usable_password())
        self.assertEqual(len(mail.outbox), 1)
        body = mail.outbox[0].body
        self.assertEqual(mail.outbox[0].subject, "Welcome to Debug Gym — your account is ready")
        self.assertIn("choose a password using the link below", body)
        self.assertNotIn("Initial password:", body)
        self.assertNotIn("debug-gym-pass", body)
        path = re.search(r"http://testserver(\S+)", body).group(1)
        client = Client()
        response = client.get(path)
        reset_path = response.url
        self.assertContains(client.get(reset_path), "Set password")
        response = client.post(reset_path, {
            "new_password1": "A-strong-new-pass2026", "new_password2": "A-strong-new-pass2026"
        })
        self.assertRedirects(response, reverse("accounts:login"))
        user.refresh_from_db()
        self.assertTrue(user.check_password("A-strong-new-pass2026"))
        self.assertContains(Client().get(path, follow=True), "invalid or expired")

    @override_settings(
        ACCOUNT_EMAIL_ENABLED=True, ACCOUNT_PUBLIC_URL="http://testserver",
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    )
    def test_csv_emails_after_success_only_and_skips_unchanged_reimport(self):
        csv = "name,email\nInvited,invited@example.com\n"
        self.assertEqual(self.upload(csv).status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(self.upload(csv).status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(self.upload(
            "name,email\nOther,other@example.com\nTeacher,teacher@example.com\n"
        ).status_code, 400)
        self.assertEqual(len(mail.outbox), 1)
        self.assertFalse(User.objects.filter(email="other@example.com").exists())

    @override_settings(
        ACCOUNT_EMAIL_ENABLED=True, ACCOUNT_PUBLIC_URL="http://testserver",
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    )
    def test_inactive_accounts_cannot_use_access_links(self):
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.encoding import force_bytes
        from django.utils.http import urlsafe_base64_encode

        token = default_token_generator.make_token(self.student)
        self.student.is_active = False
        self.student.save()
        path = reverse("accounts:set-password", kwargs={
            "uidb64": urlsafe_base64_encode(force_bytes(self.student.pk)), "token": token,
        })
        self.assertContains(Client().get(path, follow=True), "invalid or expired")

    @override_settings(ACCOUNT_EMAIL_ENABLED=False)
    def test_email_disabled_reports_failure_and_csv_needs_initial_password(self):
        response = self.client.post(reverse(
            "admin_panel:account-access-link", args=[self.student.pk]
        ), follow=True)
        self.assertContains(response, "Access email was not sent")
        self.assertEqual(self.upload("name,email\nX,x@example.com\n").status_code, 302)
        self.assertFalse(User.objects.get(email="x@example.com").has_usable_password())

    @override_settings(
        ACCOUNT_EMAIL_ENABLED=True, ACCOUNT_PUBLIC_URL="http://testserver",
        EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend",
    )
    def test_access_tokens_are_never_printed_to_console(self):
        from contextlib import redirect_stdout

        from .mail import send_access_link

        output = io.StringIO()
        with redirect_stdout(output):
            self.assertFalse(send_access_link(self.student))
            self.assertFalse(send_access_link(self.student, initial_password="not-for-logs"))
        self.assertEqual(output.getvalue(), "")
