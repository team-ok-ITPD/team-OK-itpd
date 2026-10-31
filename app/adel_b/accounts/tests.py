import json

from django.contrib.auth import get_user_model
from django.test import TestCase

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
        self.assertEqual(response.json()["user"], {"username": "adel", "email": "adel@example.com"})
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
