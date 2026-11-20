# [Admin Dev] Tests for administrator teacher-account and group-membership workflows
from django.test import TestCase
from django.urls import reverse

from django.utils import timezone

from core.models import Assignment, AssignmentGroup, Bug, GroupStudent, StudyGroup, User


class AdminPanelTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user("admin@example.com", "Admin", "debug-gym-pass", role=User.Role.ADMIN)
        self.teacher = User.objects.create_user("teacher@example.com", "Teacher", "debug-gym-pass", role=User.Role.PROFESSOR)
        self.student = User.objects.create_user("student@example.com", "Student", "debug-gym-pass")
        self.group = StudyGroup.objects.create(name="Python A", professor=self.teacher)

    def login_admin(self):
        self.client.force_login(self.admin)

    def test_admin_edits_students_and_other_administrators(self):
        other_admin = User.objects.create_user(
            "other-admin@example.com", "Other admin", "old-password", role=User.Role.ADMIN
        )
        self.login_admin()
        for account, route, listing in (
            (self.student, "student-edit", "students"),
            (other_admin, "administrator-edit", "administrators"),
        ):
            with self.subTest(route=route):
                url = reverse(f"admin_panel:{route}", args=[account.pk])
                self.assertContains(
                    self.client.get(reverse(f"admin_panel:{listing}")), f'href="{url}"'
                )
                self.assertContains(self.client.get(url), account.email)
                response = self.client.post(url, {
                    "name": "Updated name", "email": f"updated-{account.pk}@example.com",
                    "is_active": "on", "password": "replacement-password",
                    "password_confirmation": "replacement-password",
                    "role": User.Role.PROFESSOR,
                })
                self.assertRedirects(response, reverse(f"admin_panel:{listing}"))
                old_role = account.role
                account.refresh_from_db()
                self.assertEqual(account.name, "Updated name")
                self.assertEqual(account.email, f"updated-{account.pk}@example.com")
                self.assertEqual(account.role, old_role)
                self.assertTrue(account.check_password("replacement-password"))
                response = self.client.post(url, {
                    "name": account.name, "email": account.email,
                    "password": "", "password_confirmation": "",
                })
                self.assertRedirects(response, reverse(f"admin_panel:{listing}"))
                account.refresh_from_db()
                self.assertFalse(account.is_active)
                self.assertTrue(account.check_password("replacement-password"))

    def test_account_edit_routes_are_role_scoped_and_admin_only(self):
        for route, target, wrong_target in (
            ("student-edit", self.student, self.admin),
            ("administrator-edit", self.admin, self.student),
        ):
            self.login_admin()
            self.assertEqual(self.client.get(
                reverse(f"admin_panel:{route}", args=[wrong_target.pk])
            ).status_code, 404)
            url = reverse(f"admin_panel:{route}", args=[target.pk])
            for account in (None, self.student, self.teacher):
                self.client.logout()
                if account:
                    self.client.force_login(account)
                for method in ("get", "post"):
                    self.assertEqual(getattr(self.client, method)(url).status_code,
                                     403 if account else 302)

    def test_account_edits_reject_duplicate_emails_and_mismatched_passwords(self):
        self.login_admin()
        for route, account in (
            ("student-edit", self.student), ("administrator-edit", self.admin),
        ):
            for overrides in (
                {"email": self.teacher.email.upper()},
                {"password": "replacement-password", "password_confirmation": "different"},
            ):
                payload = {"name": account.name, "email": account.email, "is_active": "on",
                           "password": "", "password_confirmation": ""}
                payload.update(overrides)
                response = self.client.post(
                    reverse(f"admin_panel:{route}", args=[account.pk]), payload
                )
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context["form"].errors)
                original_email = account.email
                account.refresh_from_db()
                self.assertEqual(account.email, original_email)

    def test_admin_cannot_deactivate_self_and_self_password_change_keeps_session(self):
        self.login_admin()
        url = reverse("admin_panel:administrator-edit", args=[self.admin.pk])
        payload = {"name": self.admin.name, "email": self.admin.email,
                   "password": "", "password_confirmation": ""}
        response = self.client.post(url, payload)
        self.assertContains(response, "You cannot deactivate your own administrator account.")
        self.admin.refresh_from_db()
        self.assertTrue(self.admin.is_active)
        payload.update(is_active="on", password="replacement-password",
                       password_confirmation="replacement-password")
        self.assertRedirects(self.client.post(url, payload), reverse("admin_panel:administrators"))
        self.admin.refresh_from_db()
        self.assertTrue(self.admin.check_password("replacement-password"))
        self.assertEqual(self.client.get(reverse("admin_panel:dashboard")).status_code, 200)

    def test_student_and_administrator_edits_require_csrf(self):
        from django.test import Client

        client = Client(enforce_csrf_checks=True)
        client.force_login(self.admin)
        for route, account in (
            ("student-edit", self.student), ("administrator-edit", self.admin),
        ):
            self.assertEqual(client.post(
                reverse(f"admin_panel:{route}", args=[account.pk]), {}
            ).status_code, 403)

    def test_admin_creates_teacher_account(self):
        self.login_admin()
        response = self.client.post(reverse("admin_panel:user-create"), {"name": "New Teacher", "email": "new@example.com", "is_active": "on", "password": "new-password", "password_confirmation": "new-password"})
        self.assertRedirects(response, reverse("admin_panel:users"))
        teacher = User.objects.get(email="new@example.com")
        self.assertEqual(teacher.role, User.Role.PROFESSOR)
        self.assertTrue(teacher.check_password("new-password"))

    def test_admin_creates_each_account_role_without_payload_role_override(self):
        self.login_admin()
        for route, role, destination in (
            ("user-create", User.Role.PROFESSOR, "users"),
            ("student-create", User.Role.STUDENT, "students"),
            ("administrator-create", User.Role.ADMIN, "administrators"),
        ):
            with self.subTest(role=role):
                email = f"new-{role}@example.com"
                response = self.client.post(reverse(f"admin_panel:{route}"), {
                    "name": f"New {role}", "email": email, "is_active": "on",
                    "password": "new-password", "password_confirmation": "new-password",
                    "role": User.Role.ADMIN if role != User.Role.ADMIN else User.Role.STUDENT,
                })
                self.assertRedirects(response, reverse(f"admin_panel:{destination}"))
                account = User.objects.get(email=email)
                self.assertEqual(account.role, role)
                self.assertTrue(account.check_password("new-password"))
                self.assertNotEqual(account.password, "new-password")

    def test_account_creation_validates_passwords_and_case_insensitive_email(self):
        self.login_admin()
        for route in ("user-create", "student-create", "administrator-create"):
            for overrides in (
                {"email": "invalid-email"},
                {"email": self.teacher.email.upper()},
                {"password_confirmation": "different-password"},
                {"password": "short", "password_confirmation": "short"},
            ):
                with self.subTest(route=route, overrides=overrides):
                    before = User.objects.count()
                    payload = {
                        "name": "New account", "email": "unique@example.com",
                        "is_active": "on", "password": "new-password",
                        "password_confirmation": "new-password",
                    }
                    payload.update(overrides)
                    response = self.client.post(reverse(f"admin_panel:{route}"), payload)
                    self.assertEqual(response.status_code, 200)
                    self.assertTrue(response.context["form"].errors)
                    self.assertEqual(User.objects.count(), before)

    def test_admin_creates_group_assigns_teacher_and_enrolls_student(self):
        self.login_admin()
        response = self.client.post(reverse("admin_panel:group-create"), {
            "name": "New group", "description": "Python", "professor": self.teacher.pk,
        })
        group = StudyGroup.objects.get(name="New group")
        self.assertRedirects(response, reverse("admin_panel:group-detail", args=[group.pk]))
        self.assertEqual(group.professor, self.teacher)
        response = self.client.post(reverse("admin_panel:group-member-add", args=[group.pk]),
                                    {"student": self.student.pk})
        self.assertRedirects(response, reverse("admin_panel:group-detail", args=[group.pk]))
        self.assertTrue(group.students.filter(pk=self.student.pk).exists())

    def test_admin_can_assign_another_teacher_without_changing_memberships(self):
        teacher = User.objects.create_user("other@example.com", "Other", "password",
                                           role=User.Role.PROFESSOR)
        self.group.students.add(self.student)
        bug = Bug.objects.create(
            title="Owned exercise", description="Original ownership",
            buggy_code="pass", solution_code="pass", language="python",
            created_by=self.teacher,
        )
        assignment = Assignment.objects.create(
            title="Owned assignment", bug=bug, professor=self.teacher
        )
        assignment.groups.add(self.group)
        self.login_admin()
        response = self.client.post(reverse("admin_panel:group-edit", args=[self.group.pk]), {
            "name": self.group.name, "description": "", "professor": teacher.pk,
        })
        self.assertRedirects(response, reverse("admin_panel:group-detail", args=[self.group.pk]))
        self.group.refresh_from_db()
        self.assertEqual(self.group.professor, teacher)
        self.assertTrue(self.group.students.filter(pk=self.student.pk).exists())
        assignment.refresh_from_db()
        bug.refresh_from_db()
        self.assertEqual(assignment.professor, self.teacher)
        self.assertEqual(bug.created_by, self.teacher)

    def test_group_teacher_must_be_an_active_professor(self):
        inactive = User.objects.create_user("inactive@example.com", "Inactive", "password",
                                            role=User.Role.PROFESSOR, is_active=False)
        self.login_admin()
        for invalid_teacher in (self.admin, self.student, inactive):
            for route, args in (("group-create", []), ("group-edit", [self.group.pk])):
                with self.subTest(role=invalid_teacher.role, route=route):
                    response = self.client.post(reverse(f"admin_panel:{route}", args=args), {
                        "name": "Invalid group", "professor": invalid_teacher.pk,
                    })
                    self.assertEqual(response.status_code, 200)
                    self.assertIn("professor", response.context["form"].errors)
        self.group.refresh_from_db()
        self.assertEqual(self.group.professor, self.teacher)
        self.assertFalse(StudyGroup.objects.filter(name="Invalid group").exists())

    def test_provisioning_and_group_mutations_require_admin(self):
        urls = [
            reverse(f"admin_panel:{route}") for route in
            ("user-create", "student-create", "administrator-create", "group-create")
        ] + [
            reverse("admin_panel:group-edit", args=[self.group.pk]),
            reverse("admin_panel:group-member-add", args=[self.group.pk]),
            reverse("admin_panel:group-member-remove", args=[self.group.pk, self.student.pk]),
        ]
        for account in (None, self.student, self.teacher):
            self.client.logout()
            if account:
                self.client.force_login(account)
            for url in urls:
                for method in ("get", "post"):
                    with self.subTest(account=account, url=url, method=method):
                        response = getattr(self.client, method)(url)
                        self.assertEqual(response.status_code, 403 if account else 302)

    def test_new_management_pages_render_and_link_to_actions(self):
        self.login_admin()
        for route, content in (
            ("students", "Create student"),
            ("administrators", "Create administrator"),
            ("student-create", "Save student"),
            ("administrator-create", "Save administrator"),
            ("group-create", "Save group"),
        ):
            with self.subTest(route=route):
                self.assertContains(self.client.get(reverse(f"admin_panel:{route}")), content)
        self.assertContains(self.client.get(reverse("admin_panel:groups")), "Create group")
        self.assertContains(
            self.client.get(reverse("admin_panel:group-detail", args=[self.group.pk])),
            "Edit group / assign teacher",
        )

    def test_all_admin_pages_require_admin_including_direct_urls(self):
        urls = [
            reverse(f"admin_panel:{route}") for route in (
                "dashboard", "users", "students", "administrators", "user-create",
                "student-create", "administrator-create", "groups", "group-create",
                "assignments",
            )
        ] + [
            reverse("admin_panel:user-edit", args=[self.teacher.pk]),
            reverse("admin_panel:group-detail", args=[self.group.pk]),
            reverse("admin_panel:group-edit", args=[self.group.pk]),
            reverse("admin_panel:assignment-detail", args=[999]),
        ]
        for account in (None, self.student, self.teacher):
            self.client.logout()
            if account:
                self.client.force_login(account)
            for url in urls:
                with self.subTest(account=account, url=url):
                    self.assertEqual(self.client.get(url).status_code, 403 if account else 302)

    def test_teacher_edit_preserves_password_and_role_and_rejects_role_injection(self):
        self.login_admin()
        response = self.client.post(reverse("admin_panel:user-edit", args=[self.teacher.pk]), {
            "name": "Updated teacher", "email": "updated@example.com", "is_active": "on",
            "password": "", "password_confirmation": "", "role": User.Role.ADMIN,
        })
        self.assertRedirects(response, reverse("admin_panel:users"))
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.name, "Updated teacher")
        self.assertEqual(self.teacher.role, User.Role.PROFESSOR)
        self.assertTrue(self.teacher.check_password("debug-gym-pass"))
        self.assertEqual(
            self.client.get(reverse("admin_panel:user-edit", args=[self.admin.pk])).status_code,
            404,
        )

    def test_duplicate_and_inactive_students_are_rejected(self):
        self.group.students.add(self.student)
        inactive = User.objects.create_user(
            "inactive-student@example.com", "Inactive", "password", is_active=False
        )
        self.login_admin()
        for student in (self.student, inactive, self.admin, self.teacher):
            with self.subTest(student=student):
                response = self.client.post(
                    reverse("admin_panel:group-member-add", args=[self.group.pk]),
                    {"student": student.pk},
                )
                self.assertEqual(response.status_code, 400)
        self.assertEqual(self.group.students.count(), 1)

    def test_membership_changes_are_post_only_and_scoped_to_group(self):
        self.group.students.add(self.student)
        other_group = StudyGroup.objects.create(name="Other group", professor=self.teacher)
        self.login_admin()
        for route, args in (
            ("group-member-add", [self.group.pk]),
            ("group-member-remove", [self.group.pk, self.student.pk]),
        ):
            self.assertEqual(
                self.client.get(reverse(f"admin_panel:{route}", args=args)).status_code, 405
            )
        response = self.client.post(reverse(
            "admin_panel:group-member-remove", args=[other_group.pk, self.student.pk]
        ))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(self.group.students.filter(pk=self.student.pk).exists())

    def test_account_lists_are_role_scoped_searchable_and_paginated(self):
        User.objects.bulk_create([
            User(name=f"Learner {index:02}", email=f"learner{index}@example.com",
                 role=User.Role.STUDENT) for index in range(21)
        ])
        self.login_admin()
        for route, visible, hidden in (
            ("students", self.student.email, self.teacher.email),
            ("administrators", self.admin.email, self.student.email),
        ):
            with self.subTest(route=route):
                response = self.client.get(reverse(f"admin_panel:{route}"), {"q": visible.upper()})
                self.assertContains(response, visible)
                self.assertNotContains(response, hidden)
                response = self.client.get(reverse(f"admin_panel:{route}"), {"q": "missing"})
                self.assertContains(response, "No accounts match")
        response = self.client.get(reverse("admin_panel:students"))
        self.assertEqual(len(response.context["accounts"]), 20)
        self.assertContains(response, "?page=2")
        response = self.client.get(reverse("admin_panel:students"), {"page": 2})
        self.assertEqual(len(response.context["accounts"]), 2)

    def test_mutations_require_csrf_token(self):
        from django.test import Client

        client = Client(enforce_csrf_checks=True)
        client.force_login(self.admin)
        for route in ("user-create", "student-create", "administrator-create", "group-create"):
            with self.subTest(route=route):
                self.assertEqual(client.post(reverse(f"admin_panel:{route}"), {}).status_code, 403)

    def test_admin_management_pages_render(self):
        self.login_admin()
        for url, content in (
            (reverse("admin_panel:dashboard"), "Teacher accounts"),
            (reverse("admin_panel:users"), self.teacher.email),
            (reverse("admin_panel:groups"), self.group.name),
            (reverse("admin_panel:group-detail", args=[self.group.pk]), "Add student"),
            (reverse("admin_panel:assignments"), "Assignment visibility"),
        ):
            with self.subTest(url=url):
                self.assertContains(self.client.get(url), content)

    def test_non_admin_is_forbidden(self):
        self.client.force_login(self.student)
        for url in (
            reverse("admin_panel:groups"),
            reverse("admin_panel:assignments"),
        ):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 403)

    def test_deactivated_teacher_is_forbidden(self):
        self.teacher.is_active = False
        self.teacher.save()
        self.client.force_login(self.teacher)
        response = self.client.get(reverse("professor:dashboard"))
        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('professor:dashboard')}",
        )

    def test_admin_deactivates_teacher_from_account_form(self):
        self.login_admin()
        response = self.client.post(
            reverse("admin_panel:user-edit", args=[self.teacher.pk]),
            {
                "name": self.teacher.name,
                "email": self.teacher.email,
                "password": "",
                "password_confirmation": "",
            },
        )
        self.assertRedirects(response, reverse("admin_panel:users"))
        self.teacher.refresh_from_db()
        self.assertFalse(self.teacher.is_active)

    def test_assignments_are_read_only_context_with_group_names(self):
        bug = Bug.objects.create(
            title="Off-by-one",
            description="Fix the loop boundary.",
            buggy_code="for index in range(1): pass",
            solution_code="for index in range(2): pass",
            language="python",
            difficulty=Bug.Difficulty.EASY,
            visibility=Bug.Visibility.PRIVATE,
            created_by=self.teacher,
        )
        assignment = Assignment.objects.create(
            title="Loop exercise",
            bug=bug,
            professor=self.teacher,
            deadline=timezone.now(),
        )
        AssignmentGroup.objects.create(assignment=assignment, group=self.group)

        self.login_admin()
        response = self.client.get(reverse("admin_panel:assignments"))

        self.assertContains(response, assignment.title)
        self.assertContains(response, self.group.name)
        self.assertNotContains(response, "Edit assignment")
        self.assertNotContains(response, "<th>Exercise</th>", html=True)
        detail_url = reverse("admin_panel:assignment-detail", args=[assignment.pk])
        self.assertContains(self.client.get(detail_url), assignment.title)
        self.assertContains(self.client.get(detail_url), bug.title)
        self.assertEqual(self.client.post(detail_url, {"title": "Changed"}).status_code, 405)
        assignment.refresh_from_db()
        self.assertEqual(assignment.title, "Loop exercise")

    def test_admin_adds_and_removes_student(self):
        self.login_admin()
        response = self.client.post(reverse("admin_panel:group-member-add", args=[self.group.pk]), {"student": self.student.pk})
        self.assertRedirects(response, reverse("admin_panel:group-detail", args=[self.group.pk]))
        self.assertTrue(GroupStudent.objects.filter(group=self.group, student=self.student).exists())
        response = self.client.post(reverse("admin_panel:group-member-remove", args=[self.group.pk, self.student.pk]))
        self.assertRedirects(response, reverse("admin_panel:group-detail", args=[self.group.pk]))
        self.assertFalse(GroupStudent.objects.filter(group=self.group, student=self.student).exists())

    def test_admin_cannot_edit_student_or_add_teacher_to_group(self):
        self.login_admin()
        self.assertEqual(self.client.get(reverse("admin_panel:user-edit", args=[self.student.pk])).status_code, 404)
        response = self.client.post(
            reverse("admin_panel:group-member-add", args=[self.group.pk]),
            {"student": self.teacher.pk},
        )
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Select a valid choice", status_code=400)
        self.assertFalse(GroupStudent.objects.filter(group=self.group, student=self.teacher).exists())

    def test_group_search_has_a_distinct_no_match_state(self):
        self.login_admin()
        response = self.client.get(reverse("admin_panel:groups"), {"q": "missing"})
        self.assertContains(response, "No groups match")
        self.assertNotContains(response, "No teaching groups yet.")

    def test_teacher_and_assignment_search_have_distinct_no_match_states(self):
        self.login_admin()
        for url, label, empty_label in (
            (reverse("admin_panel:users"), "No teachers match", "No teacher accounts yet."),
            (reverse("admin_panel:assignments"), "No assignments match", "No assignments yet."),
        ):
            with self.subTest(url=url):
                response = self.client.get(url, {"q": "missing"})
                self.assertContains(response, label)
                self.assertNotContains(response, empty_label)
