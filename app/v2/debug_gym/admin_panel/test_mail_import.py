# [Admin Dev] Functional account email and CSV import regressions
import io
import csv
from unittest.mock import patch

from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from core.models import GroupStudent, StudyGroup, User


@override_settings(
    ACCOUNT_EMAIL_ENABLED=True,
    ACCOUNT_PUBLIC_URL="http://testserver",
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    DEFAULT_FROM_EMAIL="service@example.test",
)
class MailImportFunctionalTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user("admin@example.test", "Administrator", role="admin")
        self.teacher = User.objects.create_user("teacher@example.test", "Teacher", role="professor")
        self.client.force_login(self.admin)
        self.url = reverse("admin_panel:student-import")

    def upload(self, text, *, confirm=True, client=None):
        return (client or self.client).post(self.url, {
            "file": SimpleUploadedFile("students.csv", text.encode("utf-8"), content_type="text/csv"),
            **({"confirm": "on"} if confirm else {}),
        })

    def test_csv_legacy_password_never_changes_existing_account(self):
        student = User.objects.create_user("existing@example.test", "Existing", "Old-pass-456!")
        response = self.upload("name,email,password\nExisting,existing@example.test,New-pass-456!\n")
        self.assertEqual(response.status_code, 302)
        student.refresh_from_db()
        self.assertTrue(student.check_password("Old-pass-456!"))
        self.assertEqual(len(mail.outbox), 0)

    def test_csv_invitation_repeat_preserves_owner_password_and_ignores_legacy_cells(self):
        csv = "name,email,password\nInvited,invited@example.test,x\n"
        self.assertEqual(self.upload(csv).status_code, 302)
        student = User.objects.get(email="invited@example.test")
        self.assertFalse(student.has_usable_password())
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("/accounts/set-password/", mail.outbox[0].body)
        student.set_password("Owner-chosen-456!")
        student.save()
        original_hash = student.password
        self.assertEqual(self.upload(csv).status_code, 302)
        student.refresh_from_db()
        self.assertEqual(student.password, original_hash)
        self.assertTrue(student.check_password("Owner-chosen-456!"))
        self.assertEqual(len(mail.outbox), 1)

    def test_csv_mixed_creation_and_password_update_choose_correct_templates(self):
        User.objects.create_user("existing@example.test", "Existing", "Old-pass-456!")
        response = self.upload(
            "name,email,password\nNew,new@example.test,\nExisting,existing@example.test,New-pass-456!\n"
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        messages = {message.to[0]: message for message in mail.outbox}
        self.assertIn("Welcome", messages["new@example.test"].subject)
        self.assertNotIn("existing@example.test", messages)
        self.assertTrue(User.objects.get(email="existing@example.test").check_password("Old-pass-456!"))

    def test_csv_quoted_unicode_bom_and_multiple_memberships_are_repeatable(self):
        text = io.StringIO()
        text.write("\ufeff")
        writer = csv.writer(text)
        writer.writerow(["name", "email", "course", "group_number", "teacher_email"])
        for number in ("01", "02"):
            writer.writerow(["Иван, студент", "MixedCase@Example.Test", "Python", number, self.teacher.email])
        self.assertEqual(self.upload(text.getvalue()).status_code, 302)
        student = User.objects.get(email__iexact="MixedCase@Example.Test")
        self.assertEqual(student.name, "Иван, студент")
        self.assertFalse(student.has_usable_password())
        self.assertEqual(GroupStudent.objects.filter(student=student).count(), 2)
        self.assertEqual(StudyGroup.objects.count(), 2)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(self.upload(text.getvalue()).status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(GroupStudent.objects.count(), 2)

    def test_late_invalid_row_rolls_back_created_group_student_and_mail(self):
        response = self.upload(
            "name,email,course,group_number,teacher_email\n"
            f"New,new@example.test,Python,01,{self.teacher.email}\n"
            "Bad,not-an-email,,,\n"
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(email="new@example.test").exists())
        self.assertFalse(StudyGroup.objects.exists())
        self.assertEqual(len(mail.outbox), 0)

    def test_csv_requires_confirmation_and_admin_role(self):
        text = "name,email\nNew,new@example.test\n"
        self.assertEqual(self.upload(text, confirm=False).status_code, 400)
        for role in ("student", "professor"):
            user = User.objects.create_user(f"{role}@example.test", role, role=role)
            client = Client()
            client.force_login(user)
            self.assertEqual(self.upload(text, client=client).status_code, 403)
        self.assertFalse(User.objects.filter(email="new@example.test").exists())
        self.assertEqual(len(mail.outbox), 0)

    def test_csv_and_manual_resend_require_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.admin)
        self.assertEqual(self.upload("name,email\nNew,new@example.test\n", client=client).status_code, 403)
        self.assertEqual(client.post(
            reverse("admin_panel:account-access-link", args=[self.teacher.pk]),
        ).status_code, 403)
        self.assertEqual(len(mail.outbox), 0)

    def test_import_failure_does_not_reveal_any_password(self):
        response = self.upload(
            "name,email,password\nNew,new@example.test,Private-row-password!\n"
            "Other,admin@example.test,Other-private-password!\n"
        )
        self.assertEqual(response.status_code, 400)
        self.assertNotContains(response, "Private-row-password!", status_code=400)
        self.assertNotContains(response, "Other-private-password!", status_code=400)
        self.assertFalse(User.objects.filter(email="new@example.test").exists())
        self.assertEqual(len(mail.outbox), 0)

    def test_delivery_failure_keeps_import_and_allows_manual_resend(self):
        with patch("admin_panel.mail.send_mail", side_effect=RuntimeError("private SMTP details")):
            response = self.upload("name,email\nNew,new@example.test\n")
        self.assertEqual(response.status_code, 302)
        student = User.objects.get(email="new@example.test")
        page = self.client.get(response.url)
        self.assertContains(page, "Some access emails were not sent")
        self.assertNotContains(page, "private SMTP details")
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(self.client.post(
            reverse("admin_panel:account-access-link", args=[student.pk]),
        ).status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Debug Gym — your password setup link")

    def test_normal_emails_have_no_preview_markers_and_use_trusted_origin(self):
        with override_settings(PASSWORD_RESET_TIMEOUT=3600):
            response = self.upload("name,email\nNew,new@example.test\n")
        self.assertEqual(response.status_code, 302)
        message = mail.outbox[0]
        self.assertEqual(message.from_email, "service@example.test")
        self.assertIn("expires in 1 hour and", message.body)
        self.assertIn("http://testserver/accounts/set-password/", message.body)
        self.assertNotIn("[TEST", message.subject)
        self.assertNotIn("TEST PREVIEW", message.body)
        self.assertNotIn("email-preview", message.body)

    def test_inactive_import_sends_no_mail_or_resend(self):
        self.assertEqual(self.upload(
            "name,email,is_active\nInactive,inactive@example.test,false\n"
        ).status_code, 302)
        student = User.objects.get(email="inactive@example.test")
        self.assertFalse(student.is_active)
        self.assertEqual(self.client.post(
            reverse("admin_panel:account-access-link", args=[student.pk]),
        ).status_code, 302)
        self.assertEqual(len(mail.outbox), 0)
