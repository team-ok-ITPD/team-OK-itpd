# [Backend Dev] Tests for login and logout
from io import StringIO

from django.core.management import call_command
from django.test import TestCase, override_settings
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

    def test_professor_and_admin_go_to_their_dashboards(self):
        User.objects.create_user("sara@example.com", "Sara", PASSWORD, role=User.Role.PROFESSOR)
        self.assertRedirects(self.login(email="sara@example.com"), reverse("professor:dashboard"))
        self.client.logout()
        User.objects.create_superuser("root@example.com", "Root", PASSWORD)
        self.assertRedirects(self.login(email="root@example.com"), reverse("admin_panel:dashboard"))

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


@override_settings(DEMO_LOGIN=True)
class DemoLoginTests(TestCase):
    url = reverse("accounts:login")

    def setUp(self):
        out = StringIO()
        call_command("seed_demo", stdout=out)

    def test_buttons_show_one_account_per_role(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Demo accounts")
        for label in ("Sign in as Admin", "Sign in as Professor", "Sign in as Student"):
            self.assertContains(response, label)
        self.assertEqual([d["label"] for d in response.context["demo_logins"]], ["Admin", "Professor", "Student"])

    def test_each_button_signs_in_to_its_dashboard(self):
        cases = {
            "admin@demo.debuggym.test": "admin_panel:dashboard",
            "prof.karim@demo.debuggym.test": "professor:dashboard",
            "ali@demo.debuggym.test": "student:dashboard",
        }
        for email, dashboard in cases.items():
            demo = next(d for d in self.client.get(self.url).context["demo_logins"] if d["user"].email == email)
            response = self.client.post(self.url, {"username": email, "password": demo["password"]})
            self.assertRedirects(response, reverse(dashboard), fetch_redirect_response=False)
            self.client.logout()

    @override_settings(DEMO_LOGIN=False)
    def test_hidden_when_turned_off(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, "Demo accounts")
        self.assertNotContains(response, "demo-pass")

    def test_hidden_without_demo_data(self):
        call_command("seed_demo", "--delete", stdout=StringIO())
        self.assertNotContains(self.client.get(self.url), "Demo accounts")

    def test_hidden_when_signed_in(self):
        self.client.force_login(User.objects.get(email="ali@demo.debuggym.test"))
        self.assertNotContains(self.client.get(self.url), "Demo accounts")
