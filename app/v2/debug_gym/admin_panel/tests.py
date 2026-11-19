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

    def test_admin_creates_teacher_account(self):
        self.login_admin()
        response = self.client.post(reverse("admin_panel:user-create"), {"name": "New Teacher", "email": "new@example.com", "is_active": "on", "password": "new-password", "password_confirmation": "new-password"})
        self.assertRedirects(response, reverse("admin_panel:users"))
        teacher = User.objects.get(email="new@example.com")
        self.assertEqual(teacher.role, User.Role.PROFESSOR)
        self.assertTrue(teacher.check_password("new-password"))

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
