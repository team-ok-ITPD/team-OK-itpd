# [Backend Dev] Tests for login and logout
from django.test import TestCase
from django.urls import reverse

from core.models import User

PASSWORD = "debug-gym-pass"


class LoginTests(TestCase):
    url = reverse("accounts:login")

    def setUp(self):
        self.student = User.objects.create_user("ali@example.com", "Ali", PASSWORD)

    def login(self, email="ali@example.com", password=PASSWORD, **extra):
        return self.client.post(self.url, {"username": email, "password": password, **extra})

    def test_root_and_login_page(self):
        self.assertRedirects(self.client.get("/"), self.url)
        response = self.client.get(self.url)
        self.assertContains(response, "Sign in")
        self.assertContains(response, 'type="email"')
        self.assertContains(response, "css/main.css")

    def test_wrong_password_shows_an_error(self):
        response = self.login(password="wrong-password")
        self.assertContains(response, "That email and password do not match")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_deactivated_account_cannot_log_in(self):
        self.student.is_active = False
        self.student.save()
        response = self.login()
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertEqual(response.status_code, 200)

    def test_login_with_any_email_case(self):
        response = self.login(email="ALI@Example.com")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.student.id)

    def test_login_redirects_a_student_to_their_dashboard(self):
        self.assertRedirects(self.login(), "/student/")

    def test_each_role_reaches_its_own_dashboard(self):
        cases = (
            (User.Role.ADMIN, "/admin-panel/"),
            (User.Role.PROFESSOR, "/professor/"),
            (User.Role.STUDENT, "/student/"),
        )
        for role, url in cases:
            with self.subTest(role=role):
                user = User.objects.create_user(
                    f"{role}@example.com", role.title(), PASSWORD, role=role
                )
                self.client.force_login(user)
                self.assertEqual(self.client.get(url).status_code, 200)
                self.client.logout()

    def test_anonymous_dashboard_request_redirects_to_login(self):
        response = self.client.get("/student/")
        self.assertRedirects(response, f"{self.url}?next=/student/")

    def test_a_role_cannot_open_another_role_dashboard(self):
        self.client.force_login(self.student)
        self.assertEqual(self.client.get("/professor/").status_code, 403)

    def test_student_navigation_has_only_the_student_dashboard(self):
        self.client.force_login(self.student)
        response = self.client.get("/student/")
        self.assertContains(response, 'href="/student/"')
        self.assertContains(response, "My practice")
        self.assertContains(response, "Sign out")
        self.assertNotContains(response, 'href="/professor/"')
        self.assertNotContains(response, 'href="/admin-panel/"')

    def test_safe_next_link_is_followed(self):
        response = self.login(next="/django-admin/")
        self.assertEqual(response["Location"], "/django-admin/")

    def test_outside_next_link_is_ignored(self):
        response = self.login(next="https://evil.example.com/")
        self.assertEqual(response["Location"], "/student/")

    def test_logout(self):
        self.login()
        response = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(response, self.url)
        self.assertNotIn("_auth_user_id", self.client.session)
