# [Backend Dev] Credential, authoring, verification and agent review regressions
from datetime import timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import hashlib
import json

from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .agents import AgentError, api_key, save_key
from .models import (
    AgentCredential, Assignment, Bug, StudyGroup, Submission, User,
    WorkspacePairingCode, WorkspaceSession,
)
from .projects import ProjectError, validate_project
from .runtime import RuntimeError


class IntegrationTests(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user("teacher@test.example", "Teacher", role="professor")
        self.student = User.objects.create_user("student@test.example", "Student", role="student")
        self.other = User.objects.create_user("other@test.example", "Other", role="professor")
        self.group = StudyGroup.objects.create(name="Lab", professor=self.teacher)
        self.group.students.add(self.student)
        self.bug = Bug.objects.create(
            title="Counter", description="Fix the result", language="python", difficulty="easy",
            visibility="private", created_by=self.teacher, entry_file="main.py",
            buggy_code="def count(): return 0",
            project_files={
                "main.py": "def count(): return 0",
                "test_main.py": "from main import count\ndef test_count(): assert count() == 1\n",
            },
        )
        self.assignment = Assignment.objects.create(
            title="Lab assignment", professor=self.teacher, bug=self.bug,
        )
        self.assignment.groups.add(self.group)
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        config = override_settings(
            DEBUG_GYM_KEY_FILE=Path(temporary.name) / "key",
            DEBUG_GYM_WORKSPACES_DIR=Path(temporary.name) / "workspaces",
            DEBUG_GYM_AGENT_KEY="",
        )
        config.enable()
        self.addCleanup(config.disable)

    def token(self, author=False):
        raw = "author-token" if author else "student-token"
        session = WorkspaceSession.objects.create(
            user=self.teacher if author else self.student, bug=self.bug,
            assignment=None if author else self.assignment, authoring=author,
            revision=self.bug.revision,
            token_digest=hashlib.sha256(raw.encode()).hexdigest(),
            expires_at=timezone.now() + timedelta(hours=1),
        )
        return raw, session

    def send(self, token, **data):
        payload = {"bug": self.bug.pk, "code": "def count(): return 1", **data}
        return self.client.post(
            "/api/ide/submit/", json.dumps(payload), content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )

    def test_pairing_code_is_single_use_and_creates_a_scoped_submission_session(self):
        code = WorkspacePairingCode.issue(
            self.student, self.bug, self.assignment, "http://localhost:8000/student/assignments/1/"
        )
        response = self.client.post(
            "/api/ide/pair/",
            json.dumps({"code": f"{code[:8]}-{code[8:]}".lower()}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["files"], self.bug.project_files)
        self.assertEqual(payload["exercise"]["entryFile"], "main.py")
        self.assertTrue(payload["exercise"]["tests"])
        self.assertNotIn("solution_code", json.dumps(payload))
        pairing = WorkspacePairingCode.objects.get()
        self.assertNotEqual(pairing.code_digest, code)
        self.assertIsNotNone(pairing.used_at)
        session = WorkspaceSession.objects.get()
        self.assertEqual(session.user, self.student)
        self.assertEqual(session.bug, self.bug)
        self.assertEqual(session.assignment, self.assignment)
        self.assertEqual(
            session.token_digest, hashlib.sha256(payload["token"].encode()).hexdigest()
        )

        with patch("core.workspace_api.verify", return_value=(1, 2)):
            submitted = self.send(payload["token"])
        self.assertEqual(submitted.status_code, 200)
        self.assertEqual(submitted.json()["attempt"]["passed"], 1)
        self.assertEqual(Submission.objects.count(), 1)

        reused = self.client.post(
            "/api/ide/pair/", json.dumps({"code": code}), content_type="application/json"
        )
        self.assertEqual(reused.status_code, 401)

    def test_pairing_code_expires_and_rechecks_assignment_access(self):
        expired = WorkspacePairingCode.issue(
            self.student, self.bug, self.assignment, "http://localhost:8000/"
        )
        expired_row = WorkspacePairingCode.objects.get()
        expired_row.expires_at = timezone.now() - timedelta(seconds=1)
        expired_row.save(update_fields=("expires_at",))
        response = self.client.post(
            "/api/ide/pair/", json.dumps({"code": expired}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)
        self.assertFalse(WorkspaceSession.objects.exists())

        active = WorkspacePairingCode.issue(
            self.student, self.bug, self.assignment, "http://localhost:8000/"
        )
        self.group.students.remove(self.student)
        response = self.client.post(
            "/api/ide/pair/", json.dumps({"code": active}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)
        self.assertFalse(WorkspaceSession.objects.exists())

    def test_pairing_includes_legacy_test_code(self):
        bug = Bug.objects.create(
            title="Legacy test field", description="Find the issue", language="python",
            difficulty="easy", visibility="public", created_by=self.teacher,
            buggy_code="def solve(): return False",
            tests_code="from main import solve\ndef test_solve(): assert solve()\n",
        )
        code = WorkspacePairingCode.issue(self.student, bug, None, "http://localhost:8000/")
        response = self.client.post(
            "/api/ide/pair/", json.dumps({"code": code}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["files"]["test_main.py"], bug.tests_code)
        self.assertTrue(response.json()["exercise"]["tests"])

    def test_local_pairing_allows_submission_when_exercise_has_no_tests(self):
        bug = Bug.objects.create(
            title="Exercise without tests", description="Fix the result", language="python",
            difficulty="easy", visibility="public", created_by=self.teacher,
            buggy_code="def solve(): return False",
        )
        code = WorkspacePairingCode.issue(self.student, bug, None, "http://localhost:8000/")
        paired = self.client.post(
            "/api/ide/pair/", json.dumps({"code": code}), content_type="application/json"
        )
        self.assertEqual(paired.status_code, 200)
        self.assertFalse(paired.json()["exercise"]["tests"])

        with patch("core.workspace_api.verify") as verify:
            response = self.client.post(
                "/api/ide/submit/",
                json.dumps({"bug": bug.pk, "code": "def solve(): return True"}),
                content_type="application/json",
                headers={"Authorization": f"Bearer {paired.json()['token']}"},
            )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["attempt"]["verified"])
        verify.assert_not_called()
        submission = Submission.objects.get(bug=bug)
        self.assertIsNone(submission.tests_passed)
        self.assertIsNone(submission.tests_total)

    def test_encrypted_key_and_platform_fallback(self):
        save_key(self.teacher, "personal-key")
        record = AgentCredential.objects.get(user=self.teacher)
        self.assertNotIn("personal-key", record.encrypted_key)
        self.assertEqual(api_key(self.teacher), "personal-key")
        with override_settings(DEBUG_GYM_AGENT_KEY="platform-key"):
            self.assertEqual(api_key(self.teacher), "personal-key")
            save_key(self.teacher, "")
            self.assertEqual(api_key(self.teacher), "platform-key")
        with self.assertRaises(AgentError):
            api_key(self.teacher)

    def test_settings_never_echo_the_key(self):
        self.client.force_login(self.teacher)
        self.client.post(reverse("professor:settings"), {"key": "private-test-key", "provider": "openai"})
        page = self.client.get(reverse("professor:settings"))
        self.assertContains(page, "Personal key saved")
        self.assertNotContains(page, "private-test-key")
        self.client.force_login(self.student)
        self.assertEqual(self.client.get(reverse("professor:settings")).status_code, 403)

    @patch("core.workspace_api.verify", return_value=(1, 2))
    def test_student_callback_verifies_and_deduplicates(self, verify):
        token, session = self.token()
        for _ in range(2):
            response = self.send(token, passed=999, total=999)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["attempt"]["passed"], 1)
        self.assertEqual(Submission.objects.count(), 1)
        self.assertEqual(verify.call_count, 1)
        self.assertEqual(Submission.objects.get().tests_total, 2)

    @patch("core.workspace_api.verify")
    def test_closed_expired_and_changed_assignment_are_rejected(self, verify):
        token, session = self.token()
        self.assignment.status = "closed"
        self.assignment.save()
        self.assertEqual(self.send(token).status_code, 403)
        verify.assert_not_called()
        self.assignment.status = "active"
        self.assignment.save()
        self.bug.revision += 1
        self.bug.save()
        verify.return_value = (1, 1)
        self.assertEqual(self.send(token).status_code, 409)
        self.assertFalse(Submission.objects.exists())
        session.expires_at = timezone.now() - timedelta(seconds=1)
        session.save()
        self.assertEqual(self.send(token).status_code, 403)

    @patch("core.workspace_api.verify")
    def test_callback_rechecks_deadline_after_verification(self, verify):
        token, _ = self.token()
        def close(*args):
            Assignment.objects.filter(pk=self.assignment.pk).update(status="closed")
            return 1, 1
        verify.side_effect = close
        self.assertEqual(self.send(token).status_code, 403)
        self.assertFalse(Submission.objects.exists())

    def test_author_callback_persists_project_and_blocks_stale_sessions(self):
        token, _ = self.token(author=True)
        files = {**self.bug.project_files, "main.py": "def count(): return 2"}
        response = self.send(token, code=files["main.py"], files=files)
        self.assertEqual(response.status_code, 200)
        self.bug.refresh_from_db()
        self.assertEqual(self.bug.project_files, files)
        self.assertEqual(self.bug.revision, 2)
        self.assertEqual(self.send(token, code=files["main.py"], files=files).status_code, 200)
        self.bug.refresh_from_db()
        self.assertEqual(self.bug.revision, 2)
        files["main.py"] = "def count(): return 3"
        self.bug.revision = 3
        self.bug.save()
        self.assertEqual(self.send(token, code=files["main.py"], files=files).status_code, 409)

    def test_author_snapshot_cannot_write_session_metadata(self):
        token, _ = self.token(author=True)
        files = {**self.bug.project_files, ".debug-gym/config.json": "{}"}
        self.assertEqual(self.send(token, files=files).status_code, 400)
        self.bug.refresh_from_db()
        self.assertNotIn(".debug-gym/config.json", self.bug.project_files)

    @patch("core.workspace_api.open_workspace", return_value="http://localhost:9000")
    def test_launch_checks_teacher_ownership_and_student_membership(self, launch):
        url = reverse("workspace-launch", args=[self.bug.pk])
        self.client.force_login(self.other)
        self.assertEqual(self.client.post(url, {"mode": "author"}).status_code, 403)
        self.client.force_login(self.teacher)
        self.assertEqual(self.client.post(url, {"mode": "author"}).status_code, 200)
        self.client.force_login(self.student)
        self.assertEqual(self.client.post(url, {}).status_code, 403)
        self.assertEqual(self.client.post(url, {"assignment": self.assignment.pk}).status_code, 200)
        self.group.students.clear()
        self.assertEqual(self.client.post(url, {"assignment": self.assignment.pk}).status_code, 403)

    @patch("core.workspace_api.verify", side_effect=RuntimeError("Docker unavailable"))
    def test_failed_verification_never_fabricates_counts(self, verify):
        token, _ = self.token()
        self.assertEqual(self.send(token).status_code, 400)
        self.assertFalse(Submission.objects.exists())

    @patch("professor.agent_tasks.verify", return_value=(0, 1))
    @patch("professor.agent_tasks.ask_agent")
    def test_generation_validates_bug_tests_and_assigns_group(self, agent, verify):
        agent.return_value = {
            "title": "Generated counter", "description": "Fix this",
            "entry_file": "main.py", "project_files": self.bug.project_files,

        }
        self.client.force_login(self.teacher)
        response = self.client.post(reverse("professor:generate"), {
            "prompt": "Count correctly", "language": "python", "test_count": 1, "group": self.group.pk,
        })
        self.assertRedirects(response, reverse("professor:group", args=[self.group.pk]))
        generated = Bug.objects.get(title="Generated counter")
        self.assertEqual(generated.visibility, "private")
        self.assertEqual(generated.assignments.get().groups.get(), self.group)

    @patch("professor.agent_tasks.verify", return_value=(1, 1))
    @patch("professor.agent_tasks.ask_agent")
    def test_generator_rejects_a_bug_that_already_passes(self, agent, verify):
        agent.return_value = {
            "title": "Invalid generated", "description": "Fix this",
            "entry_file": "main.py", "project_files": self.bug.project_files,

        }
        self.client.force_login(self.teacher)
        page = self.client.post(reverse("professor:generate"), {
            "prompt": "Generate", "language": "python", "test_count": 1,
        })
        self.assertContains(page, "Generated tests did not validate")
        self.assertFalse(Bug.objects.filter(title="Invalid generated").exists())

    @patch("professor.agent_tasks.ask_agent")
    @override_settings(DEBUG_GYM_AGENT_KEY="test-key")
    def test_review_is_gated_and_saves_advisory_findings(self, agent):
        from professor.reviews import run_review
        submission = Submission.objects.create(
            student=self.student, assignment=self.assignment, bug=self.bug,
            submitted_code="hardcoded", tests_passed=1, tests_total=1,
        )
        agent.return_value = {"reviews": [{
            "submission_id": submission.pk, "suspicious": True, "reason": "Hardcodes the example.",
        }]}
        self.assertEqual(run_review(self.assignment), "waiting")
        agent.assert_not_called()
        self.assignment.status = "closed"
        self.assignment.save()
        self.assertEqual(run_review(self.assignment), "completed")
        submission.refresh_from_db()
        self.assertEqual(submission.suspicion_status, "review")
        self.assertIsNotNone(submission.reviewed_at)
        self.assertNotIn(self.student.email, json.dumps(agent.call_args.args, default=str))
        agent.return_value = {"reviews": []}
        self.assertEqual(run_review(self.assignment), "completed")
        self.assertEqual(agent.call_count, 1)
        submission.refresh_from_db()
        self.assertEqual(submission.suspicion_reason, "Hardcodes the example.")

    def test_student_progress_returns_only_own_submission(self):
        Submission.objects.create(
            student=self.student, bug=self.bug, assignment=self.assignment,
            submitted_code="fixed", tests_passed=1, tests_total=2,
        )
        self.client.force_login(self.student)
        url = reverse("student:progress", args=[self.bug.pk])
        response = self.client.get(url, {"assignment": self.assignment.pk})
        self.assertEqual(response.json()["passed"], 1)
        self.assertNotIn("fixed", response.content.decode())
        self.group.students.clear()
        self.assertEqual(self.client.get(url, {"assignment": self.assignment.pk}).status_code, 404)

    @patch("core.agents.urlopen")
    def test_agent_uses_personal_key_and_hides_provider_failures(self, opened):
        from urllib.error import URLError
        from core.agents import ask_agent

        save_key(self.teacher, "personal-test-key")
        opened.return_value.__enter__.return_value.read.return_value = json.dumps({
            "choices": [{"message": {"content": '{"ok":true}'}}],
        }).encode()
        with override_settings(DEBUG_GYM_AGENT_KEY="internal-test-key"):
            self.assertEqual(ask_agent(self.teacher, "Task", {}), {"ok": True})
        request = opened.call_args.args[0]
        self.assertEqual(request.get_header("Authorization"), "Bearer personal-test-key")
        opened.side_effect = URLError("private-provider-error-with-a-key")
        with self.assertRaises(AgentError) as failure:
            ask_agent(self.teacher, "Task", {})
        self.assertNotIn("private-provider", str(failure.exception))

    @patch("core.runtime.start_ide", return_value=9000)
    def test_reopening_workspace_preserves_unsaved_source(self, start):
        from core.runtime import open_workspace

        token, session = self.token(author=True)
        open_workspace(session, token)
        from django.conf import settings
        source = settings.DEBUG_GYM_WORKSPACES_DIR / str(session.pk) / "main.py"
        source.write_text("unsaved change", encoding="utf-8")
        open_workspace(session, token)
        self.assertEqual(source.read_text(), "unsaved change")

    @override_settings(DEBUG_GYM_AGENT_KEY="test-key")
    @patch("professor.reviews.analyze")
    def test_scheduled_review_covers_all_attempts_once(self, analyze):
        from professor.reviews import review_due_assignments
        from core.models import AssignmentReview

        rows = [
            Submission.objects.create(
                assignment=self.assignment, bug=self.bug,
                student=self.student, submitted_code=f"attempt {index}",
            ) for index in range(3)
        ]
        analyze.return_value = {row.pk: (False, "No issues observed.") for row in rows}
        review_due_assignments()
        analyze.assert_not_called()
        self.assignment.deadline = timezone.now() - timedelta(seconds=1)
        self.assignment.save()
        review_due_assignments()
        review_due_assignments()
        analyze.assert_called_once()
        self.assertEqual([row.pk for row in analyze.call_args.args[2]], [row.pk for row in rows])
        self.assertEqual(AssignmentReview.objects.get(assignment=self.assignment).status, "completed")
        self.assertEqual(Submission.objects.filter(reviewed_at__isnull=False).count(), 3)

    @patch("professor.reviews.analyze")
    def test_missing_key_keeps_review_pending(self, analyze):
        from professor.reviews import review_due_assignments
        from core.models import AssignmentReview

        self.assignment.status = "closed"
        self.assignment.save()
        review_due_assignments()
        self.assertFalse(AssignmentReview.objects.exists())
        analyze.assert_not_called()

    @override_settings(DEBUG_GYM_AGENT_KEY="test-key")
    @patch("professor.reviews.analyze", side_effect=AgentError("Provider timeout."))
    def test_failed_review_is_not_sent_again(self, analyze):
        from professor.reviews import run_review
        from core.models import AssignmentReview

        self.assignment.status = "closed"
        self.assignment.save()
        Submission.objects.create(
            assignment=self.assignment, student=self.student, bug=self.bug, submitted_code="fixed",
        )
        self.assertEqual(run_review(self.assignment), "failed")
        self.assertEqual(run_review(self.assignment), "failed")
        analyze.assert_called_once()
        self.assertEqual(AssignmentReview.objects.get().status, "failed")

    @patch("core.runtime.verify", return_value=(1, 2))
    def test_demo_seed_is_additive_and_repeatable(self, verify):
        from django.core.management import call_command
        from django.conf import settings
        import io

        with TemporaryDirectory() as directory, override_settings(BASE_DIR=Path(directory)):
            for _ in range(2):
                call_command("seed_teaching_demo", teacher=self.teacher.email, stdout=io.StringIO())
            self.assertEqual(StudyGroup.objects.filter(professor=self.teacher, name__startswith="Demo").count(), 2)
            self.assertEqual(Bug.objects.filter(created_by=self.teacher, title__startswith="Demo").count(), 2)
            self.assertEqual(Assignment.objects.filter(professor=self.teacher, title__startswith="Demo").count(), 4)


class RuntimeReportTests(SimpleTestCase):
    @patch("core.runtime.docker.from_env")
    def test_report_is_read_before_temporary_container_is_removed(self, docker):
        from core.runtime import verify

        container = docker.return_value.containers.run.return_value
        container.wait.return_value = {"StatusCode": 1}
        container.logs.return_value = [b'<testsuites><testsuite><testcase name="one"/><testcase name="two"><failure/></testcase></testsuite></testsuites>']
        bug = Bug(
            language="python", entry_file="main.py", buggy_code="original",
            project_files={"main.py": "original", "test_main.py": "test source"},
        )
        self.assertEqual(verify(bug, "fixed"), (1, 2))
        container.remove.assert_called_once_with(force=True)
        kwargs = docker.return_value.containers.run.call_args.kwargs
        self.assertTrue(kwargs["network_disabled"])
        self.assertTrue(kwargs["read_only"])
        self.assertEqual(kwargs["cap_drop"], ["ALL"])

    @patch("core.runtime.docker.from_env")
    def test_invalid_report_is_not_a_passing_result(self, docker):
        from core.runtime import verify

        container = docker.return_value.containers.run.return_value
        container.wait.return_value = {"StatusCode": 0}
        container.logs.return_value = [b"invalid report"]
        bug = Bug(
            language="javascript", entry_file="main.js", buggy_code="original",
            project_files={"main.js": "original", "main.test.js": "test source"},
        )
        with self.assertRaises(RuntimeError):
            verify(bug, "fixed")
        container.remove.assert_called_once_with(force=True)
