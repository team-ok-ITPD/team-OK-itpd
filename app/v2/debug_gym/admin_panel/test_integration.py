# [Admin Dev] Cross-role account, assignment, submission and access regression checks
from datetime import timedelta
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

from django.test import Client, SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import timezone

from core.models import Assignment, Bug, StudyGroup, Submission, User, WorkspaceSession
from student.models import IdeToken


class SharedIdeSettingsTests(SimpleTestCase):
    def test_both_launchers_honor_workspace_and_image_environment(self):
        root = Path(__file__).resolve().parents[1]
        workspace = root / "test-settings-only-not-created"
        environment = {
            **os.environ,
            "DEBUG_GYM_WORKSPACES_DIR": str(workspace),
            "DEBUG_GYM_IDE_IMAGE": "integration-test-image",
        }
        result = subprocess.run(
            [sys.executable, "-c", (
                "import json; from config import settings as s; "
                "print(json.dumps([str(s.WORKSPACES_DIR), str(s.DEBUG_GYM_WORKSPACES_DIR), "
                "s.DEBUG_GYM_IDE_IMAGE]))"
            )],
            cwd=root, env=environment, check=True, capture_output=True, text=True,
        )
        self.assertEqual(json.loads(result.stdout), [
            str(workspace), str(workspace), "integration-test-image",
        ])


class CrossRoleWorkflowTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user("admin@example.com", "Admin", role="admin")
        self.teacher = User.objects.create_user("teacher@example.com", "Teacher", role="professor")
        self.group = StudyGroup.objects.create(
            name="Integration course", group_number="045", professor=self.teacher,
        )
        self.bug = Bug.objects.create(
            title="Integration exercise", description="Fix it", buggy_code="broken",
            solution_code="fixed", language="python", created_by=self.teacher,
            visibility=Bug.Visibility.PRIVATE,
        )
        self.client.force_login(self.admin)
        self.teacher_client = Client()
        self.teacher_client.force_login(self.teacher)
        response = self.client.post(reverse("admin_panel:student-create"), {
            "name": "Integration Student", "email": "learner@example.com",
            "password": "Integration-2026!", "is_active": "on",
        })
        self.assertEqual(response.status_code, 302)
        self.student = User.objects.get(email="learner@example.com")
        self.student_client = Client()
        self.student_client.force_login(self.student)
        response = self.teacher_client.post(reverse("professor:assign", args=[self.group.pk]), {
            "bug": self.bug.pk, "title": "Cross-role assignment", "deadline": "",
        })
        self.assertEqual(response.status_code, 302)
        self.assignment = Assignment.objects.get(title="Cross-role assignment")

    def batch(self, action):
        return self.client.post(reverse("admin_panel:student-batch"), {
            "students": [self.student.pk], "action": action, "group": self.group.pk,
        })

    def submit(self, token):
        return self.student_client.post(
            reverse("student:ide_submit"), json.dumps({
                "code": "fixed", "tests_passed": 999, "tests_total": 999,
            }), content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )

    def workspace_token(self):
        token = "cross-role-workspace-token"
        WorkspaceSession.objects.create(
            user=self.student, bug=self.bug, assignment=self.assignment,
            revision=self.bug.revision,
            token_digest=hashlib.sha256(token.encode()).hexdigest(),
            expires_at=timezone.now() + timedelta(hours=1),
        )
        return token

    def test_enrollment_submission_results_and_removal(self):
        detail = reverse("student:assignment_detail", args=[self.assignment.pk])
        self.assertEqual(self.student_client.get(detail).status_code, 404)
        self.assertEqual(self.batch("add").status_code, 302)
        self.assertEqual(self.student_client.get(detail).status_code, 200)
        token = IdeToken.issue(self.student, self.bug, self.assignment)
        self.assertEqual(self.submit(token).status_code, 201)
        submission = Submission.objects.get(assignment=self.assignment, student=self.student)
        self.assertIsNone(submission.tests_passed)
        self.assertIsNone(submission.tests_total)
        workspace_token = self.workspace_token()
        self.assertEqual(self.batch("remove").status_code, 302)
        self.assertEqual(self.student_client.get(detail).status_code, 404)
        self.assertEqual(self.submit(token).status_code, 403)
        with patch("core.workspace_api.verify") as verify:
            response = self.student_client.post(
                reverse("ide-submit"), json.dumps({"bug": self.bug.pk, "code": "fixed"}),
                content_type="application/json",
                headers={"Authorization": f"Bearer {workspace_token}"},
            )
        self.assertEqual(response.status_code, 403)
        verify.assert_not_called()
        self.assertTrue(Submission.objects.filter(pk=submission.pk).exists())
        self.assertEqual(self.batch("add").status_code, 302)
        self.assertEqual(self.student_client.get(detail).status_code, 200)
        self.assertEqual(Submission.objects.filter(assignment=self.assignment).count(), 1)
        response = self.teacher_client.post(reverse(
            "professor:close", args=[self.group.pk, self.assignment.pk],
        ))
        self.assertEqual(response.status_code, 302)
        results = self.teacher_client.get(reverse(
            "professor:assignment", args=[self.group.pk, self.assignment.pk],
        ))
        self.assertContains(results, self.student.email)
        self.assertContains(results, "Awaiting verification")
        self.assertEqual(self.submit(token).status_code, 403)

    def test_deactivation_revokes_both_ide_tokens_and_web_session(self):
        self.assertEqual(self.batch("add").status_code, 302)
        token = IdeToken.issue(self.student, self.bug, self.assignment)
        workspace_token = self.workspace_token()
        self.assertEqual(self.batch("deactivate").status_code, 302)
        self.student.refresh_from_db()
        self.assertFalse(self.student.is_active)
        self.assertFalse(IdeToken.objects.filter(student=self.student).exists())
        self.assertFalse(WorkspaceSession.objects.filter(user=self.student).exists())
        self.assertEqual(self.student_client.get(reverse("student:dashboard")).status_code, 302)
        self.assertEqual(self.submit(token).status_code, 401)
        self.assertEqual(self.batch("activate").status_code, 302)
        self.student.refresh_from_db()
        self.assertTrue(self.student.is_active)
        self.assertTrue(self.group.students.filter(pk=self.student.pk).exists())
        self.assertEqual(self.submit(token).status_code, 401)
        response = self.student_client.post(
            reverse("ide-submit"), json.dumps({"bug": self.bug.pk, "code": "fixed"}),
            content_type="application/json",
            headers={"Authorization": f"Bearer {workspace_token}"},
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.teacher_client.get(reverse("professor:dashboard")).status_code, 200)
        self.assertEqual(self.client.get(reverse("admin_panel:students")).status_code, 200)
