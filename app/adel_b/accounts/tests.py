import json

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.test import RequestFactory, TestCase

from .models import Profile, is_professor, role_of
from .permissions import professor_required_json

User = get_user_model()


class AccountTests(TestCase):
    def post(self, url, payload):
        return self.client.post(url, data=json.dumps(payload), content_type="application/json")

    def register(self, **overrides):
        payload = {"username": "adel", "email": "adel@example.com", "password": "debug-gym-pass"}
        payload.update(overrides)
        return self.post("/api/auth/register/", payload)

    def test_register_logs_in(self):
        response = self.register(email="Adel@Example.com")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["user"], {"username": "adel", "email": "adel@example.com", "role": "student"}
        )
        self.assertEqual(self.client.get("/api/auth/me/").json()["user"]["username"], "adel")
        user = User.objects.get(username="adel")
        self.assertNotEqual(user.password, "debug-gym-pass")
        self.assertTrue(user.check_password("debug-gym-pass"))

    def test_register_requires_all_fields(self):
        self.assertEqual(self.register(email="").status_code, 400)

    def test_register_rejects_taken_username_and_email(self):
        self.register()
        self.client.logout()
        response = self.register(username="ADEL", email="ADEL@example.com")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.json()["fields"]), {"username", "email"})

    def test_register_rejects_bad_email_and_weak_password(self):
        response = self.register(email="not-an-email", password="1234")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.json()["fields"]), {"email", "password"})
        self.assertFalse(User.objects.exists())

    def test_register_rejects_bad_username(self):
        response = self.register(username="has space")
        self.assertEqual(response.status_code, 400)
        self.assertIn("username", response.json()["fields"])

    def test_login_with_username_or_email(self):
        self.register()
        self.client.logout()
        self.assertEqual(self.post("/api/auth/login/", {"login": "adel", "password": "debug-gym-pass"}).status_code, 200)
        self.client.logout()
        response = self.post("/api/auth/login/", {"login": "ADEL@example.com", "password": "debug-gym-pass"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["user"]["username"], "adel")

    def test_login_rejects_wrong_password_and_unknown_user(self):
        self.register()
        self.client.logout()
        for login in ("adel", "nobody", "nobody@example.com"):
            response = self.post("/api/auth/login/", {"login": login, "password": "wrong-password"})
            self.assertEqual(response.status_code, 400)
        self.assertIsNone(self.client.get("/api/auth/me/").json()["user"])

    def test_logout(self):
        self.register()
        self.assertEqual(self.post("/api/auth/logout/", {}).status_code, 200)
        self.assertIsNone(self.client.get("/api/auth/me/").json()["user"])


class RoleTests(TestCase):
    def make(self, username, role=None):
        user = User.objects.create_user(username=username, email=f"{username}@example.com", password="debug-gym-pass")
        if role:
            user.profile.role = role
            user.profile.save()
        return user

    def test_new_accounts_are_students(self):
        user = self.make("new")
        self.assertEqual(user.profile.role, Profile.STUDENT)
        self.assertFalse(is_professor(user))

    def test_register_cannot_choose_professor(self):
        response = self.client.post(
            "/api/auth/register/",
            data=json.dumps({"username": "sneaky", "email": "s@example.com", "password": "debug-gym-pass", "role": "professor"}),
            content_type="application/json",
        )
        self.assertEqual(response.json()["user"]["role"], "student")
        self.assertEqual(User.objects.get(username="sneaky").profile.role, Profile.STUDENT)

    def test_me_and_login_report_a_professor(self):
        self.make("prof", Profile.PROFESSOR)
        response = self.client.post(
            "/api/auth/login/", data=json.dumps({"login": "prof", "password": "debug-gym-pass"}), content_type="application/json"
        )
        self.assertEqual(response.json()["user"]["role"], "professor")
        self.assertEqual(self.client.get("/api/auth/me/").json()["user"]["role"], "professor")

    def test_user_without_profile_counts_as_student(self):
        user = self.make("old")
        Profile.objects.filter(user=user).delete()
        user = User.objects.get(pk=user.pk)
        self.assertEqual(role_of(user), Profile.STUDENT)

    def test_admin_can_change_the_role(self):
        admin = User.objects.create_superuser("boss", "boss@example.com", "debug-gym-pass")
        student = self.make("future_prof")
        self.client.force_login(admin)
        response = self.client.post(
            f"/admin/accounts/profile/",
            data={
                "form-TOTAL_FORMS": "2", "form-INITIAL_FORMS": "2", "form-MIN_NUM_FORMS": "0", "form-MAX_NUM_FORMS": "1000",
                "form-0-id": str(admin.profile.id), "form-0-role": "student",
                "form-1-id": str(student.profile.id), "form-1-role": "professor",
                "_save": "Save",
            },
        )
        self.assertEqual(response.status_code, 302)
        student.profile.refresh_from_db()
        self.assertEqual(student.profile.role, Profile.PROFESSOR)


class ProfessorOnlyTests(TestCase):
    def setUp(self):
        self.view = professor_required_json(lambda request: JsonResponse({"ok": True}))
        self.factory = RequestFactory()

    def call(self, user=None):
        from django.contrib.auth.models import AnonymousUser

        request = self.factory.post("/")
        request.user = user or AnonymousUser()
        return self.view(request)

    def test_logged_out_is_401(self):
        self.assertEqual(self.call().status_code, 401)

    def test_student_is_403(self):
        student = User.objects.create_user("stu", "stu@example.com", "debug-gym-pass")
        self.assertEqual(self.call(student).status_code, 403)

    def test_professor_is_allowed(self):
        prof = User.objects.create_user("prof", "prof@example.com", "debug-gym-pass")
        prof.profile.role = Profile.PROFESSOR
        prof.profile.save()
        self.assertEqual(self.call(prof).status_code, 200)
