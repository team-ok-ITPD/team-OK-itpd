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

    def test_student_goes_to_student_dashboard(self):
        self.assertRedirects(self.login(), reverse("student:dashboard"))

    def test_professor_goes_to_professor_dashboard(self):
        User.objects.create_user("sara@example.com", "Sara", PASSWORD, role=User.Role.PROFESSOR)
        self.assertRedirects(
            self.login(email="sara@example.com"), reverse("professor:dashboard"),
        )

    def test_safe_next_link_is_followed(self):
        response = self.login(next="/django-admin/")
        self.assertEqual(response["Location"], "/django-admin/")

    def test_outside_next_link_is_ignored(self):
        response = self.login(next="https://evil.example.com/")
        self.assertEqual(response["Location"], reverse("student:dashboard"))

    def test_logout(self):
        self.login()
        response = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(response, self.url)
        self.assertNotIn("_auth_user_id", self.client.session)
