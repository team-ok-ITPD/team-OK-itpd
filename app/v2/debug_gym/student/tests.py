# [Student Dev] Tests for the student pages
import json
import os
import shutil
import tempfile
import threading
import urllib.error
from datetime import timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from core.models import Assignment, Bug, StudyGroup, Submission, User
from student import ai, ide
from student.ide import IdeError
from student.models import IdeToken
from app.adel_b.bugs.verification import VerificationBusy
from core.runtime import RuntimeError as VerificationError

PASSWORD = "debug-gym-pass"


class StudentTestCase(TestCase):
    """Shared data: Ali and Omar in Group A, Sara as their professor, one private bug."""

    url = reverse("student:dashboard")

    def setUp(self):
        verifier = patch("student.views.verify", return_value=(1, 1))
        verifier.start()
        self.addCleanup(verifier.stop)
        self.student = User.objects.create_user("ali@example.com", "Ali", PASSWORD)
        self.other = User.objects.create_user("omar@example.com", "Omar", PASSWORD)
        self.prof = User.objects.create_user(
            "sara@example.com", "Sara", PASSWORD, role=User.Role.PROFESSOR
        )
        self.group = StudyGroup.objects.create(name="Group A", professor=self.prof)
        self.group.students.add(self.student, self.other)
        self.other_group = StudyGroup.objects.create(name="Group B", professor=self.prof)
        self.bug = Bug.objects.create(
            title="Off by one",
            description="Loop skips the last item",
            buggy_code="for i in range(len(x) - 1): pass",
            solution_code="for i in range(len(x)): pass",
            language="python",
            difficulty=Bug.Difficulty.EASY,
            visibility=Bug.Visibility.PRIVATE,
            created_by=self.prof,
        )

    def assignment(self, title, group=None, days=3, **extra):
        a = Assignment.objects.create(
            title=title,
            bug=self.bug,
            professor=self.prof,
            deadline=timezone.now() + timedelta(days=days),
            **extra,
        )
        a.groups.add(group or self.group)
        return a

    def get(self, user=None):
        self.client.force_login(user or self.student)
        return self.client.get(self.url)


class DashboardTests(StudentTestCase):
    def test_signed_out_visitor_goes_to_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={self.url}")

    def test_other_roles_are_forbidden(self):
        self.assertEqual(self.get(self.prof).status_code, 403)
        admin = User.objects.create_superuser("admin@example.com", "Admin", PASSWORD)
        self.assertEqual(self.get(admin).status_code, 403)

    def test_shows_my_groups_only(self):
        response = self.get()
        self.assertContains(response, "Welcome back, Ali")
        self.assertContains(response, "Group A")
        self.assertContains(response, "2 students")
        self.assertNotContains(response, "Group B")

    def test_pending_lists_open_unsubmitted_assignments_of_my_groups(self):
        self.assignment("Due tomorrow", days=1)
        self.assignment("Next week", days=7)
        self.assignment("Other group", group=self.other_group)
        self.assignment("Past deadline", days=-1)
        self.assignment("Closed", status=Assignment.Status.CLOSED)
        done = self.assignment("Already sent")
        Submission.objects.create(
            student=self.student, bug=self.bug, assignment=done, submitted_code="x"
        )

        pending = self.get().context["pending"]
        self.assertEqual([a.title for a in pending], ["Due tomorrow", "Next week"])
        self.assertTrue(pending[0].due_soon)
        self.assertFalse(pending[1].due_soon)

    def test_classmate_submission_does_not_hide_my_assignment(self):
        a = self.assignment("Shared")
        Submission.objects.create(student=self.other, bug=self.bug, assignment=a, submitted_code="x")
        self.assertContains(self.get(), "Shared")

    def test_recent_grades_show_only_my_graded_submissions(self):
        a = self.assignment("Graded one")
        Submission.objects.create(
            student=self.student, bug=self.bug, assignment=a, submitted_code="x",
            status=Submission.Status.GRADED, grade=9.5, feedback="Clean fix",
            graded_at=timezone.now(),
        )
        Submission.objects.create(
            student=self.other, bug=self.bug, assignment=a, submitted_code="y",
            status=Submission.Status.GRADED, grade=3, feedback="Omar feedback",
            graded_at=timezone.now(),
        )
        response = self.get()
        self.assertContains(response, "9.5")
        self.assertContains(response, "Clean fix")
        self.assertNotContains(response, "Omar feedback")
        self.assertEqual(response.context["graded_count"], 1)

    def test_empty_states(self):
        loner = User.objects.create_user("lina@example.com", "Lina", PASSWORD)
        response = self.get(loner)
        self.assertContains(response, "You are not in a group yet.")
        self.assertContains(response, "Nothing pending.")
        self.assertContains(response, "No grades yet.")

    def test_solution_code_is_never_shown(self):
        self.assignment("Due soon", days=1)
        self.assertNotContains(self.get(), self.bug.solution_code)


class AssignmentPagesTests(StudentTestCase):
    list_url = reverse("student:assignments_list")

    def detail(self, assignment, user=None):
        self.client.force_login(user or self.student)
        return self.client.get(reverse("student:assignment_detail", args=[assignment.pk]))

    def submit(self, assignment, student=None, **extra):
        return Submission.objects.create(
            student=student or self.student, bug=self.bug, assignment=assignment,
            submitted_code="fixed", **extra,
        )

    def list_statuses(self, query=""):
        self.client.force_login(self.student)
        response = self.client.get(self.list_url + query)
        return {a.title: a.my_status for a in response.context["assignments"]}

    def test_pages_need_a_student(self):
        a = self.assignment("Task")
        for url in (self.list_url, reverse("student:assignment_detail", args=[a.pk])):
            self.assertEqual(self.client.get(url).status_code, 302)
            self.client.force_login(self.prof)
            self.assertEqual(self.client.get(url).status_code, 403)
            self.client.logout()

    def test_list_shows_each_status_for_my_groups_only(self):
        self.assignment("Open")
        self.assignment("Past deadline", days=-1)
        self.assignment("Closed early", status=Assignment.Status.CLOSED)
        self.submit(self.assignment("Sent"))
        self.submit(
            self.assignment("Marked", days=-2),
            status=Submission.Status.GRADED, grade=7, graded_at=timezone.now(),
        )
        self.assignment("Other group", group=self.other_group)

        self.assertEqual(
            self.list_statuses(),
            {
                "Open": "todo",
                "Past deadline": "missed",
                "Closed early": "missed",
                "Sent": "submitted",
                "Marked": "graded",
            },
        )

    def test_status_filter_and_counts(self):
        self.assignment("Open")
        self.submit(self.assignment("Sent"))
        self.assertEqual(self.list_statuses("?status=todo"), {"Open": "todo"})
        self.assertEqual(self.list_statuses("?status=nonsense"), {"Open": "todo", "Sent": "submitted"})
        tabs = {t["key"]: t["count"] for t in self.client.get(self.list_url).context["tabs"]}
        self.assertEqual(tabs, {"": 2, "todo": 1, "submitted": 1, "graded": 0, "missed": 0})

    def test_assignment_in_two_of_my_groups_is_listed_once(self):
        self.other_group.students.add(self.student)
        a = self.assignment("Both groups")
        a.groups.add(self.other_group)
        self.assertEqual(self.list_statuses(), {"Both groups": "todo"})
        self.assertContains(self.detail(a), "Group A, Group B")

    def test_classmate_submission_does_not_change_my_status(self):
        a = self.assignment("Shared")
        self.submit(a, student=self.other, status=Submission.Status.GRADED, grade=10)
        self.assertEqual(self.list_statuses(), {"Shared": "todo"})

    def test_detail_shows_bug_without_solution(self):
        a = self.assignment("Task", instructions="Fix the loop bound.")
        response = self.detail(a)
        self.assertContains(response, "Fix the loop bound.")
        self.assertContains(response, self.bug.description)
        self.assertContains(response, self.bug.buggy_code)
        self.assertContains(response, "Not submitted yet.")
        self.assertNotContains(response, self.bug.solution_code)

    def test_detail_of_another_groups_assignment_is_404(self):
        a = self.assignment("Not mine", group=self.other_group)
        self.assertEqual(self.detail(a).status_code, 404)

    def test_detail_shows_my_grade_and_feedback_only(self):
        a = self.assignment("Task")
        self.submit(a, status=Submission.Status.GRADED, grade=8.5, feedback="Nice fix")
        self.submit(a, student=self.other, status=Submission.Status.GRADED, grade=2, feedback="Omar notes")
        response = self.detail(a)
        self.assertContains(response, "8.5")
        self.assertContains(response, "Nice fix")
        self.assertNotContains(response, "Omar notes")

    def test_detail_says_when_closed(self):
        self.assertContains(self.detail(self.assignment("Late", days=-1)), "This assignment is closed")
        self.assertNotContains(self.detail(self.assignment("Open")), "This assignment is closed")

    def test_dashboard_links_to_detail(self):
        a = self.assignment("Linked")
        self.assertContains(self.get(), reverse("student:assignment_detail", args=[a.pk]))


class WorkspaceTests(StudentTestCase):
    """The bug page and Open in VS Code (Docker is faked)."""

    def setUp(self):
        super().setUp()
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        override = override_settings(STUDENT_WORKSPACES_DIR=Path(self.tmp))
        override.enable()
        self.addCleanup(override.disable)
        self.bug.project_files = {
            "main.py": self.bug.buggy_code,
            "test_main.py": "from main import *\n\n\ndef test_x():\n    assert True\n",
        }
        self.bug.entry_file = "main.py"
        self.bug.save()

    def ws_url(self, assignment):
        return reverse("student:assignment_workspace", args=[assignment.pk])

    def open_vscode(self, assignment, user=None):
        self.client.force_login(user or self.student)
        with patch("student.views.start_ide", return_value="http://localhost:41234/?folder=/home/coder/project") as start:
            response = self.client.post(self.ws_url(assignment))
        return response, start

    def folder(self, assignment):
        return Path(self.tmp) / str(self.student.pk) / f"assignment-{assignment.pk}"

    def test_needs_a_student_in_the_group(self):
        a = self.assignment("Task")
        self.assertEqual(self.client.get(self.ws_url(a)).status_code, 302)
        self.client.force_login(self.prof)
        self.assertEqual(self.client.get(self.ws_url(a)).status_code, 403)
        other = self.assignment("Not mine", group=self.other_group)
        response, start = self.open_vscode(other)
        self.assertEqual(response.status_code, 404)
        start.assert_not_called()

    def test_page_offers_vscode_and_hides_solution(self):
        a = self.assignment("Task")
        self.client.force_login(self.student)
        page = self.client.get(self.ws_url(a))
        self.assertContains(page, "Open in VS Code</button>")
        self.assertContains(page, "<code>main.py</code>", html=False)
        self.assertContains(page, "<strong>Test</strong>", html=False)
        self.assertNotContains(page, self.bug.solution_code)
        self.assertNotContains(page, "<textarea")

    def test_open_writes_the_folder_and_redirects_to_vscode(self):
        a = self.assignment("Task")
        response, start = self.open_vscode(a)
        self.assertRedirects(response, "http://localhost:41234/?folder=/home/coder/project",
                             fetch_redirect_response=False)
        folder = self.folder(a)
        start.assert_called_once_with(self.student, folder)
        self.assertEqual((folder / "main.py").read_text(), self.bug.buggy_code + "\n")
        self.assertIn("def test_x", (folder / "test_main.py").read_text())
        config = json.loads((folder / ".debug-gym" / "config.json").read_text())
        # The address follows the port this server runs on (the test client uses 80).
        self.assertEqual(config["server"], "http://host.docker.internal:80")
        self.assertEqual(config["file"], "main.py")
        self.assertTrue(config["tests"])
        self.assertTrue(config["site"].endswith(self.ws_url(a)))
        self.assertEqual(IdeToken.find(config["token"]).assignment, a)
        self.assertNotIn(self.bug.solution_code, "".join(p.read_text() for p in folder.rglob("*") if p.is_file()))

    def test_reopening_keeps_my_edits_and_replaces_the_token(self):
        a = self.assignment("Task")
        self.open_vscode(a)
        folder = self.folder(a)
        old_token = json.loads((folder / ".debug-gym" / "config.json").read_text())["token"]
        (folder / "main.py").write_text("my work in progress\n")
        self.open_vscode(a)
        self.assertEqual((folder / "main.py").read_text(), "my work in progress\n")
        self.assertIsNone(IdeToken.find(old_token))
        self.assertEqual(IdeToken.objects.count(), 1)

    def test_first_open_starts_from_my_last_submission(self):
        a = self.assignment("Task")
        Submission.objects.create(student=self.student, bug=self.bug, assignment=a, submitted_code="mine")
        self.open_vscode(a)
        self.assertEqual((self.folder(a) / "main.py").read_text(), "mine\n")

    def test_docker_problem_is_shown_on_the_page(self):
        a = self.assignment("Task")
        self.client.force_login(self.student)
        with patch("student.views.start_ide", side_effect=IdeError("VS Code is not available: Docker is not running")):
            response = self.client.post(self.ws_url(a), follow=True)
        self.assertContains(response, "Docker is not running")

    def test_closed_work_offers_no_vscode(self):
        a = self.assignment("Late", days=-1)
        self.client.force_login(self.student)
        page = self.client.get(self.ws_url(a))
        self.assertContains(page, "The deadline has passed")
        self.assertNotContains(page, "Open in VS Code</button>")
        _, start = self.open_vscode(a)
        start.assert_not_called()

    def test_non_python_bug_has_no_tests(self):
        self.bug.language = "dart"
        self.bug.project_files = {"main.dart": "void main() {}"}
        self.bug.entry_file = "main.dart"
        self.bug.save()
        a = self.assignment("Dart task")
        self.open_vscode(a)
        folder = self.folder(a)
        self.assertTrue((folder / "main.dart").exists())
        self.assertFalse((folder / "test_main.py").exists())
        self.assertFalse(json.loads((folder / ".debug-gym" / "config.json").read_text())["tests"])

    def test_my_own_test_files_are_kept(self):
        a = self.assignment("Task")
        self.open_vscode(a)
        (self.folder(a) / "test_mine.py").write_text("def test_mine():\n    pass\n")
        self.bug.project_files = {"main.py": self.bug.buggy_code}
        self.bug.save()
        self.open_vscode(a)
        self.assertTrue((self.folder(a) / "test_mine.py").exists())
        self.assertFalse((self.folder(a) / "test_main.py").exists())

    def test_removed_tests_disappear_from_the_folder(self):
        a = self.assignment("Task")
        self.open_vscode(a)
        self.bug.project_files = {"main.py": self.bug.buggy_code}
        self.bug.save()
        self.open_vscode(a)
        self.assertFalse((self.folder(a) / "test_main.py").exists())


class IdeSubmitTests(StudentTestCase):
    """POST /student/ide/submit/ from the VS Code extension."""

    url = reverse("student:ide_submit")

    def send(self, key, code="fixed = True\n"):
        return self.client.post(
            self.url, data=json.dumps({"code": code}), content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {key}",
        )

    def mine(self, assignment=None):
        return Submission.objects.filter(student=self.student, assignment=assignment)

    def test_saves_the_fix(self):
        a = self.assignment("Task")
        response = self.send(IdeToken.issue(self.student, self.bug, a), code="line\r\n")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Fix submitted", response.json()["message"])
        submission = self.mine(a).get()
        self.assertEqual(submission.submitted_code, "line\n")
        self.assertEqual(submission.status, Submission.Status.SUBMITTED)

    def test_needs_a_valid_token(self):
        self.assignment("Task")
        self.assertEqual(self.client.post(self.url, data="{}", content_type="application/json").status_code, 401)
        self.assertEqual(self.send("not-a-real-token").status_code, 401)
        self.assertFalse(Submission.objects.exists())

    def test_blocked_after_deadline_and_when_graded(self):
        late = self.assignment("Late", days=-1)
        response = self.send(IdeToken.issue(self.student, self.bug, late))
        self.assertEqual(response.status_code, 403)
        self.assertIn("deadline has passed", response.json()["error"])
        done = self.assignment("Done")
        Submission.objects.create(student=self.student, bug=self.bug, assignment=done,
                                  submitted_code="x", status=Submission.Status.GRADED, grade=9)
        self.assertEqual(self.send(IdeToken.issue(self.student, self.bug, done)).status_code, 403)
        self.assertEqual(self.mine(late).count(), 0)
        self.assertEqual(self.mine(done).count(), 1)

    def test_losing_access_blocks_submit(self):
        a = self.assignment("Task")
        key = IdeToken.issue(self.student, self.bug, a)
        self.group.students.remove(self.student)
        self.assertEqual(self.send(key).status_code, 403)
        self.assertFalse(self.mine(a).exists())

    def test_rejects_empty_or_unchanged_code(self):
        key = IdeToken.issue(self.student, self.bug, self.assignment("Task"))
        self.assertIn("empty", self.send(key, code="  ").json()["error"])
        self.assertIn("original buggy code", self.send(key, code=self.bug.buggy_code).json()["error"])
        self.assertFalse(Submission.objects.exists())

    def test_practice_submission(self):
        public = Bug.objects.create(
            title="Public", description="d", buggy_code="x = 1", solution_code="x = 2", language="python",
            difficulty=Bug.Difficulty.EASY, visibility=Bug.Visibility.PUBLIC, created_by=self.prof,
        )
        response = self.send(IdeToken.issue(self.student, public), code="x = 2")
        self.assertEqual(response.status_code, 201)
        self.assertIn("Practice attempt saved", response.json()["message"])
        self.assertIsNone(Submission.objects.get().assignment)
        # A private bug the student cannot practise.
        self.assertEqual(self.send(IdeToken.issue(self.student, self.bug), code="y").status_code, 403)

    def with_tests(self):
        self.bug.project_files = {"main.py": self.bug.buggy_code, "test_main.py": "def test_x():\n    assert True\n"}
        self.bug.entry_file = "main.py"
        self.bug.save()

    def test_server_verification_result_is_stored(self):
        self.with_tests()
        a = self.assignment("Task")
        with patch("student.views.verify", return_value=(2, 3)) as verify:
            response = self.send(IdeToken.issue(self.student, self.bug, a))
        self.assertEqual(response.status_code, 201)
        verify.assert_called_once()
        self.assertIn("2/3 tests pass", response.json()["message"])
        self.assertEqual(self.mine(a).get().test_result, "2/3")

    def test_bug_without_tests_is_not_verified(self):
        a = self.assignment("Task")
        with patch("student.views.verify") as verify:
            self.send(IdeToken.issue(self.student, self.bug, a))
        verify.assert_not_called()
        self.assertIsNone(self.mine(a).get().tests_total)

    def test_verification_busy_or_broken_saves_nothing(self):
        self.with_tests()
        a = self.assignment("Task")
        key = IdeToken.issue(self.student, self.bug, a)
        with patch("student.views.verify", side_effect=VerificationBusy("Busy, try again.")):
            self.assertEqual(self.send(key).status_code, 503)
        with patch("student.views.verify", side_effect=VerificationError("Docker is down.")):
            self.assertEqual(self.send(key).status_code, 503)
        self.assertFalse(self.mine(a).exists())

    def test_bug_changed_during_verification_is_refused(self):
        self.with_tests()
        a = self.assignment("Task")

        def change_bug(bug, code):
            Bug.objects.filter(pk=bug.pk).update(revision=bug.revision + 1)
            return (1, 1)

        with patch("student.views.verify", side_effect=change_bug):
            response = self.send(IdeToken.issue(self.student, self.bug, a))
        self.assertEqual(response.status_code, 409)
        self.assertFalse(self.mine(a).exists())

    def test_non_student_token_is_refused(self):
        key = IdeToken.issue(self.prof, self.bug, self.assignment("Task"))
        self.assertEqual(self.send(key).status_code, 401)


class StartIdeTests(TestCase):
    """student/ide.py with a fake Docker client."""

    def setUp(self):
        self.student = User.objects.create_user("ali@example.com", "Ali", PASSWORD)
        self.docker = MagicMock()
        self.docker.errors.ImageNotFound = type("ImageNotFound", (Exception,), {})
        self.docker.errors.NotFound = type("NotFound", (Exception,), {})
        self.docker.errors.APIError = type("APIError", (Exception,), {})
        self.client_ = MagicMock()
        patcher = patch("student.ide._docker", return_value=(self.docker, self.client_))
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_missing_image_gives_a_clear_error(self):
        self.client_.images.get.side_effect = self.docker.errors.ImageNotFound()
        with self.assertRaisesMessage(ide.IdeError, "is not built on the server"):
            ide.start_ide(self.student, Path("/tmp/x"))

    def test_starts_a_locked_down_container(self):
        self.client_.containers.get.side_effect = self.docker.errors.NotFound()
        container = self.client_.containers.run.return_value
        container.ports = {ide.CONTAINER_PORT: [{"HostPort": "41234"}]}
        with patch("student.ide._wait_until_ready"):
            url = ide.start_ide(self.student, Path("/tmp/x"))
        self.assertEqual(url, "http://localhost:41234/?folder=/home/coder/project")
        kwargs = self.client_.containers.run.call_args.kwargs
        self.assertEqual(kwargs["name"], f"debug-gym-v2-ide-{self.student.pk}")
        self.assertEqual(kwargs["ports"], {ide.CONTAINER_PORT: ("127.0.0.1", None)})
        self.assertIn("no-new-privileges:true", kwargs["security_opt"])
        self.assertEqual(kwargs["mem_limit"], "512m")

    def test_reuses_a_matching_container(self):
        folder = Path("/tmp/x")
        image = self.client_.images.get.return_value
        container = self.client_.containers.get.return_value
        container.status = "running"
        container.labels = {ide.FOLDER_LABEL: str(folder), ide.SETTINGS_LABEL: ide.settings_label()}
        container.image.id = image.id
        container.ports = {ide.CONTAINER_PORT: [{"HostPort": "41000"}]}
        with patch("student.ide._wait_until_ready"):
            url = ide.start_ide(self.student, folder)
        self.assertIn(":41000/", url)
        self.client_.containers.run.assert_not_called()


class PracticeTests(StudentTestCase):
    list_url = reverse("student:public_bugs")

    def setUp(self):
        super().setUp()
        self.public = self.make_bug("Public loop", language="python", difficulty=Bug.Difficulty.EASY)
        self.dart = self.make_bug("Dart null", language="Dart", difficulty=Bug.Difficulty.HARD)

    def make_bug(self, title, **extra):
        fields = {
            "description": f"{title} description",
            "buggy_code": "x = 1",
            "solution_code": "x = 2  # SOLUTION",
            "language": "python",
            "difficulty": Bug.Difficulty.MEDIUM,
            "visibility": Bug.Visibility.PUBLIC,
            "created_by": self.prof,
            **extra,
        }
        return Bug.objects.create(title=title, **fields)

    def ws_url(self, bug):
        return reverse("student:practice_workspace", args=[bug.pk])

    def titles(self, query=""):
        self.client.force_login(self.student)
        return [b.title for b in self.client.get(self.list_url + query).context["bugs"]]

    def test_pages_need_a_student(self):
        for url in (self.list_url, self.ws_url(self.public)):
            self.assertEqual(self.client.get(url).status_code, 302)
            self.client.force_login(self.prof)
            self.assertEqual(self.client.get(url).status_code, 403)
            self.client.logout()

    def test_list_shows_public_bugs_only(self):
        # self.bug from the base fixtures is private.
        self.assertEqual(self.titles(), ["Dart null", "Public loop"])

    def test_filters(self):
        self.assertEqual(self.titles("?language=dart"), ["Dart null"])
        self.assertEqual(self.titles("?difficulty=easy"), ["Public loop"])
        self.assertEqual(self.titles("?q=LOOP"), ["Public loop"])
        self.assertEqual(self.titles("?q=description&language=python&difficulty=hard"), [])
        self.assertEqual(self.titles("?difficulty=bogus"), ["Dart null", "Public loop"])
        response = self.client.get(self.list_url + "?q=nothing-matches")
        self.assertContains(response, "No bugs match these filters.")

    def test_language_options_are_case_insensitive_and_unique(self):
        self.make_bug("Another dart", language="dart")
        self.client.force_login(self.student)
        languages = list(self.client.get(self.list_url).context["languages"])
        self.assertEqual(languages, ["dart", "python"])

    def test_private_bug_cannot_be_practised(self):
        self.client.force_login(self.student)
        self.assertEqual(self.client.get(self.ws_url(self.bug)).status_code, 404)
        self.client.post(self.ws_url(self.bug), {"code": "changed"})
        self.assertFalse(Submission.objects.exists())

    def test_practice_page_offers_vscode(self):
        self.client.force_login(self.student)
        page = self.client.get(self.ws_url(self.public))
        self.assertContains(page, "Open in VS Code</button>")
        self.assertContains(page, "Practice is not graded")
        self.assertNotContains(page, "SOLUTION")

    def test_attempt_count_is_mine_and_practice_only(self):
        Submission.objects.create(student=self.student, bug=self.public, submitted_code="a")
        Submission.objects.create(student=self.student, bug=self.public, submitted_code="b")
        Submission.objects.create(student=self.other, bug=self.public, submitted_code="c")
        a = self.assignment("Uses public bug")
        a.bug = self.public
        a.save()
        Submission.objects.create(student=self.student, bug=self.public, assignment=a, submitted_code="d")
        self.client.force_login(self.student)
        bugs = {b.title: b.my_attempts for b in self.client.get(self.list_url).context["bugs"]}
        self.assertEqual(bugs, {"Dart null": 0, "Public loop": 2})

    def test_practice_does_not_count_as_assignment_work(self):
        a = self.assignment("Task")
        Submission.objects.create(student=self.student, bug=self.bug, submitted_code="practice")
        self.client.force_login(self.student)
        statuses = {x.title: x.my_status for x in self.client.get(reverse("student:assignments_list")).context["assignments"]}
        self.assertEqual(statuses, {"Task": "todo"})


class ResultsTests(StudentTestCase):
    results_url = reverse("student:results")

    def sub(self, student=None, assignment=None, **extra):
        return Submission.objects.create(
            student=student or self.student, bug=self.bug, assignment=assignment,
            submitted_code="code", **extra,
        )

    def graded(self, grade, feedback="", student=None, title="Task"):
        return self.sub(
            student=student, assignment=self.assignment(title),
            status=Submission.Status.GRADED, grade=grade, feedback=feedback,
            graded_at=timezone.now(),
        )

    def get_results(self, query=""):
        self.client.force_login(self.student)
        return self.client.get(self.results_url + query)

    def test_needs_a_student(self):
        self.assertEqual(self.client.get(self.results_url).status_code, 302)
        self.client.force_login(self.prof)
        self.assertEqual(self.client.get(self.results_url).status_code, 403)

    def test_empty_states(self):
        response = self.get_results()
        self.assertContains(response, "No grades yet.")
        self.assertContains(response, "Nothing submitted yet.")
        self.assertIsNone(response.context["average"])

    def test_grades_feedback_and_counts_are_mine_only(self):
        self.graded(8, "Line one\nLine two", title="First")
        self.graded(9, "Great", title="Second")
        self.graded(1, "Omar only", student=self.other, title="Omar task")
        self.sub(assignment=self.assignment("Waiting"))
        self.sub()  # practice
        response = self.get_results()
        self.assertEqual(response.context["average"], 8.5)
        self.assertEqual(response.context["waiting_count"], 1)
        self.assertEqual(response.context["practice_count"], 1)
        self.assertEqual(len(response.context["graded"]), 2)
        self.assertContains(response, "Line one<br>Line two")
        self.assertNotContains(response, "Omar only")
        self.assertEqual(response.context["history"].paginator.count, 4)

    def test_history_is_paginated(self):
        for _ in range(25):
            self.sub()
        first = self.get_results()
        self.assertEqual(len(first.context["history"]), 20)
        self.assertContains(first, "Page 1 of 2")
        self.assertEqual(len(self.get_results("?page=2").context["history"]), 5)
        self.assertEqual(self.get_results("?page=junk").context["history"].number, 1)

    def test_solution_code_is_never_shown(self):
        self.graded(7)
        self.assertNotContains(self.get_results(), self.bug.solution_code)

    def test_dashboard_links_to_results(self):
        self.assertContains(self.get(), self.results_url)


class OwnBugTests(StudentTestCase):
    create_url = reverse("student:bug_create")
    list_url = reverse("student:public_bugs")

    def form_data(self, **extra):
        data = {
            "title": "My sneaky bug",
            "description": "Sum skips the last item.",
            "language": " Python ",
            "difficulty": Bug.Difficulty.EASY,
            "visibility": Bug.Visibility.PRIVATE,
            "buggy_code": "for i in range(len(x) - 1):\r\n    pass\r\n",
            "solution_code": "MY_SECRET_FIX",
        }
        data.update(extra)
        return data

    def create(self, user=None, **extra):
        self.client.force_login(user or self.student)
        return self.client.post(self.create_url, self.form_data(**extra))

    def my_bug(self, **extra):
        fields = {
            "title": "Ali bug", "description": "d", "buggy_code": "x = 1", "solution_code": "",
            "language": "python", "difficulty": Bug.Difficulty.EASY,
            "visibility": Bug.Visibility.PRIVATE, "created_by": self.student,
        }
        fields.update(extra)
        return Bug.objects.create(**fields)

    def titles(self, user, query=""):
        self.client.force_login(user)
        return [b.title for b in self.client.get(self.list_url + query).context["bugs"]]

    def test_pages_need_a_student(self):
        bug = self.my_bug()
        for url in (self.create_url, reverse("student:bug_edit", args=[bug.pk]),
                    reverse("student:bug_delete", args=[bug.pk])):
            self.client.logout()
            self.assertEqual(self.client.get(url).status_code, 302)
            self.client.force_login(self.prof)
            self.assertEqual(self.client.get(url).status_code, 403)

    def test_edit_keeps_code_exactly_as_typed(self):
        bug = self.my_bug()
        self.client.force_login(self.student)
        self.client.post(reverse("student:bug_edit", args=[bug.pk]),
                         self.form_data(buggy_code="    indented()\r\n", solution_code=""))
        bug.refresh_from_db()
        self.assertEqual(bug.buggy_code, "    indented()\n")
        self.assertEqual(bug.solution_code, "")
        self.assertEqual(bug.language, "python")
        response = self.client.post(reverse("student:bug_edit", args=[bug.pk]), self.form_data(buggy_code="   "))
        self.assertContains(response, "Add the buggy code to practise on.")

    def test_private_bug_is_only_mine(self):
        bug = self.my_bug(title="Secret one")
        self.assertIn("Secret one", self.titles(self.student))
        self.assertNotIn("Secret one", self.titles(self.other))
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(reverse("student:practice_workspace", args=[bug.pk])).status_code, 404)

    def test_public_bug_is_for_everyone(self):
        bug = self.my_bug(title="Shared one", visibility=Bug.Visibility.PUBLIC)
        self.assertIn("Shared one", self.titles(self.other))
        self.client.force_login(self.other)
        page = self.client.get(reverse("student:practice_workspace", args=[bug.pk]))
        self.assertEqual(page.status_code, 200)
        self.assertNotContains(page, "Edit my bug")

    def test_only_mine_filter(self):
        self.my_bug(title="Mine")
        Bug.objects.create(
            title="Prof public", description="d", buggy_code="x", solution_code="y",
            language="python", difficulty=Bug.Difficulty.EASY,
            visibility=Bug.Visibility.PUBLIC, created_by=self.prof,
        )
        self.assertEqual(sorted(self.titles(self.student)), ["Mine", "Prof public"])
        self.assertEqual(self.titles(self.student, "?mine=1"), ["Mine"])

    def test_edit_my_bug(self):
        bug = self.my_bug()
        self.client.force_login(self.student)
        url = reverse("student:bug_edit", args=[bug.pk])
        self.assertContains(self.client.get(url), "Save changes")
        self.client.post(url, self.form_data(title="Renamed", visibility=Bug.Visibility.PUBLIC))
        bug.refresh_from_db()
        self.assertEqual(bug.title, "Renamed")
        self.assertEqual(bug.visibility, Bug.Visibility.PUBLIC)
        self.assertEqual(bug.created_by, self.student)

    def test_cannot_edit_or_delete_someone_elses_bug(self):
        omar_bug = self.my_bug(created_by=self.other, visibility=Bug.Visibility.PUBLIC)
        self.client.force_login(self.student)
        for name in ("student:bug_edit", "student:bug_delete"):
            url = reverse(name, args=[omar_bug.pk])
            self.assertEqual(self.client.get(url).status_code, 404)
            self.assertEqual(self.client.post(url, self.form_data()).status_code, 404)
        self.assertEqual(self.client.get(reverse("student:bug_edit", args=[self.bug.pk])).status_code, 404)
        omar_bug.refresh_from_db()
        self.assertEqual(omar_bug.title, "Ali bug")

    def test_delete_asks_first_then_removes_bug_and_attempts(self):
        bug = self.my_bug(visibility=Bug.Visibility.PUBLIC)
        Submission.objects.create(student=self.student, bug=bug, submitted_code="a")
        Submission.objects.create(student=self.other, bug=bug, submitted_code="b")
        self.client.force_login(self.student)
        url = reverse("student:bug_delete", args=[bug.pk])
        page = self.client.get(url)
        self.assertContains(page, "2 practice attempts")
        self.assertContains(page, "1 other student has practised")
        self.assertTrue(Bug.objects.filter(pk=bug.pk).exists())
        self.assertRedirects(self.client.post(url), self.list_url, fetch_redirect_response=False)
        self.assertFalse(Bug.objects.filter(pk=bug.pk).exists())
        self.assertFalse(Submission.objects.filter(bug_id=bug.pk).exists())

    def test_bug_used_in_an_assignment_cannot_be_deleted(self):
        bug = self.my_bug(visibility=Bug.Visibility.PUBLIC)
        a = self.assignment("Uses student bug")
        a.bug = bug
        a.save()
        self.client.force_login(self.student)
        response = self.client.post(reverse("student:bug_delete", args=[bug.pk]))
        self.assertRedirects(response, reverse("student:bug_edit", args=[bug.pk]), fetch_redirect_response=False)
        self.assertTrue(Bug.objects.filter(pk=bug.pk).exists())


FAKE_BUG = {
    "title": "Second largest",
    "description": "Should return the second largest number, but returns the largest.",
    "buggy_code": "def second(xs):\n    return sorted(xs)[-1]\n",
    "solution_code": "def second(xs):\n    return sorted(xs)[-2]\n",
}


class AIBugTests(StudentTestCase):
    url = reverse("student:bug_create")

    def form_data(self, **extra):
        data = {
            "provider": "anthropic",
            "api_key": "sk-test-key",
            "model": "",
            "prompt": "second largest number in a list",
            "language": " Python ",
            "difficulty": Bug.Difficulty.MEDIUM,
            "visibility": Bug.Visibility.PRIVATE,
        }
        data.update(extra)
        return data

    def post(self, fake=None, **extra):
        self.client.force_login(self.student)
        with patch("student.views.ai.generate_bug", side_effect=fake or (lambda **kw: dict(FAKE_BUG))) as mocked:
            response = self.client.post(self.url, self.form_data(**extra))
        return response, mocked

    def test_needs_a_student(self):
        self.assertEqual(self.client.get(self.url).status_code, 302)
        self.client.force_login(self.prof)
        self.assertEqual(self.client.get(self.url).status_code, 403)

    def test_form_offers_providers_and_hides_nothing_secret(self):
        self.client.force_login(self.student)
        page = self.client.get(self.url)
        for label in ("Claude (Anthropic)", "OpenAI", "Google Gemini"):
            self.assertContains(page, label)
        self.assertContains(page, 'type="password"')
        self.assertContains(page, "Pick one of the public bugs")

    def test_generates_and_saves_my_bug(self):
        response, mocked = self.post()
        bug = Bug.objects.get(title="Second largest")
        self.assertRedirects(response, reverse("student:practice_workspace", args=[bug.pk]),
                             fetch_redirect_response=False)
        mocked.assert_called_once_with(
            provider="anthropic", api_key="sk-test-key", prompt="second largest number in a list",
            language="python", difficulty="medium", model="",
        )
        self.assertEqual(bug.created_by, self.student)
        self.assertEqual(bug.visibility, Bug.Visibility.PRIVATE)
        self.assertEqual(bug.language, "python")
        self.assertEqual(bug.solution_code, FAKE_BUG["solution_code"])
        page = self.client.get(response["Location"])
        self.assertContains(page, "AI created")
        self.assertNotContains(page, "sorted(xs)[-2]")  # the fix stays hidden in the workspace

    def test_public_choice_is_kept(self):
        self.post(visibility=Bug.Visibility.PUBLIC)
        self.assertEqual(Bug.objects.get(title="Second largest").visibility, Bug.Visibility.PUBLIC)

    def test_ai_error_is_shown_and_nothing_saved(self):
        def fail(**kwargs):
            raise ai.AIError("Claude rejected this API key. Check it and try again.")

        response, _ = self.post(fake=fail)
        self.assertContains(response, "Claude rejected this API key.")
        self.assertFalse(Bug.objects.filter(created_by=self.student).exists())

    def test_api_key_is_never_sent_back_or_stored(self):
        response, _ = self.post(fake=lambda **kw: (_ for _ in ()).throw(ai.AIError("boom")))
        self.assertNotContains(response, "sk-test-key")
        self.post()
        bug = Bug.objects.get(title="Second largest")
        self.assertNotIn("sk-test-key", str(vars(bug)))

    def test_required_fields(self):
        response, mocked = self.post(api_key="", prompt="")
        mocked.assert_not_called()
        self.assertEqual(set(response.context["form"].errors), {"api_key", "prompt"})


class AIClientTests(TestCase):
    """student/ai.py without any network: provider answers are faked."""

    def test_clean_result_checks_the_answer(self):
        self.assertEqual(ai.clean_result(dict(FAKE_BUG))["title"], "Second largest")
        for bad in ({}, {**FAKE_BUG, "title": 5}, {**FAKE_BUG, "buggy_code": "  "},
                    {**FAKE_BUG, "solution_code": FAKE_BUG["buggy_code"]}):
            with self.assertRaises(ai.AIError):
                ai.clean_result(bad)

    def test_unknown_provider_and_unsafe_model_name(self):
        with self.assertRaises(ai.AIError):
            ai.generate_bug("nope", "k", "p", "python", "easy")
        with self.assertRaisesMessage(ai.AIError, "model name"):
            ai.generate_bug("gemini", "k", "p", "python", "easy", model="../../other?x=1")

    def test_default_models(self):
        self.assertEqual(ai.default_model("anthropic"), "claude-opus-5-5")

    def fake_http(self, payload):
        response = MagicMock()
        response.read.return_value = json.dumps(payload).encode()
        response.__enter__.return_value = response
        return patch("student.ai.urllib.request.urlopen", return_value=response)

    def test_openai_answer_is_parsed(self):
        payload = {"choices": [{"message": {"content": json.dumps(FAKE_BUG)}}]}
        with self.fake_http(payload) as urlopen:
            result = ai.generate_bug("openai", "sk-o", "topic", "python", "easy")
        self.assertEqual(result["title"], "Second largest")
        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, "https://api.openai.com/v1/chat/completions")
        self.assertEqual(request.get_header("Authorization"), "Bearer sk-o")

    def test_gemini_answer_is_parsed(self):
        payload = {"candidates": [{"content": {"parts": [{"text": json.dumps(FAKE_BUG)}]}}]}
        with self.fake_http(payload) as urlopen:
            result = ai.generate_bug("gemini", "g-key", "topic", "dart", "hard")
        self.assertEqual(result["buggy_code"], FAKE_BUG["buggy_code"])
        self.assertIn("gemini-2.5-flash:generateContent", urlopen.call_args.args[0].full_url)

    def test_rejected_key_gives_a_clear_message(self):
        error = urllib.error.HTTPError("u", 401, "Unauthorized", {}, None)
        with patch("student.ai.urllib.request.urlopen", side_effect=error):
            with self.assertRaisesMessage(ai.AIError, "rejected this API key"):
                ai.generate_bug("openai", "bad", "topic", "python", "easy")

    def test_anthropic_answer_is_parsed(self):
        text_block = MagicMock(type="text", text=json.dumps(FAKE_BUG))
        fake_response = MagicMock(stop_reason="end_turn", content=[text_block])
        with patch("student.ai.anthropic.Anthropic") as client_class:
            client_class.return_value.beta.messages.create.return_value = fake_response
            result = ai.generate_bug("anthropic", "sk-ant", "topic", "python", "easy")
        self.assertEqual(result["title"], "Second largest")
        client_class.assert_called_once_with(api_key="sk-ant", timeout=ai.TIMEOUT_SECONDS, max_retries=1)
        kwargs = client_class.return_value.beta.messages.create.call_args.kwargs
        self.assertEqual(kwargs["model"], "claude-opus-5-5")
        self.assertEqual(kwargs["output_config"]["format"]["schema"], ai.BUG_SCHEMA)

    def test_anthropic_refusal(self):
        fake_response = MagicMock(stop_reason="refusal", content=[])
        with patch("student.ai.anthropic.Anthropic") as client_class:
            client_class.return_value.beta.messages.create.return_value = fake_response
            with self.assertRaisesMessage(ai.AIError, "declined"):
                ai.generate_bug("anthropic", "sk-ant", "topic", "python", "easy")


class BestSubmissionTests(StudentTestCase):
    """DEC-022: the submission with the most passed tests counts, not the newest."""

    def detail(self, assignment):
        self.client.force_login(self.student)
        return self.client.get(reverse("student:assignment_detail", args=[assignment.pk]))

    def attempt(self, assignment, passed=None, total=None, code="fixed", **extra):
        return Submission.objects.create(
            student=self.student, bug=self.bug, assignment=assignment,
            submitted_code=code, tests_passed=passed, tests_total=total, **extra,
        )

    def counted(self, assignment):
        self.client.force_login(self.student)
        response = self.client.get(reverse("student:assignments_list"))
        return next(a for a in response.context["assignments"] if a.pk == assignment.pk)

    def test_most_passed_tests_counts_even_when_older(self):
        a = self.assignment("Best")
        self.attempt(a, 1, 3)
        best = self.attempt(a, 3, 3)
        self.attempt(a, 2, 3)
        self.assertEqual(self.counted(a).my_submission, best)
        self.assertContains(self.detail(a), "Tests passed: 3/3")

    def test_equal_counts_newest_counts(self):
        a = self.assignment("Tie")
        self.attempt(a, 2, 3)
        newest = self.attempt(a, 2, 3)
        self.assertEqual(self.counted(a).my_submission, newest)

    def test_without_counts_latest_counts(self):
        a = self.assignment("No counts")
        self.attempt(a)
        latest = self.attempt(a)
        self.assertEqual(self.counted(a).my_submission, latest)

    def test_attempt_with_counts_beats_one_without(self):
        a = self.assignment("Mixed")
        verified = self.attempt(a, 0, 3)
        self.attempt(a)
        self.assertEqual(self.counted(a).my_submission, verified)

    def test_status_follows_the_counted_submission(self):
        a = self.assignment("Status")
        self.attempt(a, 3, 3, status=Submission.Status.GRADED, grade=9, graded_at=timezone.now())
        self.attempt(a, 1, 3)
        self.assertEqual(self.counted(a).my_status, "graded")

    def test_classmate_results_do_not_count_for_me(self):
        a = self.assignment("Mine only")
        mine = self.attempt(a, 1, 3)
        Submission.objects.create(
            student=self.other, bug=self.bug, assignment=a, submitted_code="x",
            tests_passed=3, tests_total=3,
        )
        self.assertEqual(self.counted(a).my_submission, mine)

    def test_editor_reloads_latest_code_not_the_counted_one(self):
        a = self.assignment("Editor")
        self.attempt(a, 3, 3, code="best code")
        self.attempt(a, 1, 3, code="newest code")
        self.client.force_login(self.student)
        response = self.client.get(reverse("student:assignment_workspace", args=[a.pk]))
        self.assertContains(response, "newest code")
        self.assertNotContains(response, "best code")

    def test_history_marks_the_counted_attempt(self):
        a = self.assignment("History")
        self.attempt(a, 3, 3)
        self.attempt(a, 1, 3)
        response = self.detail(a)
        self.assertContains(response, "Counted", count=1)

    def test_form_cannot_set_test_results(self):
        # Students submit from VS Code now; extra fields in the request are ignored.
        a = self.assignment("Forged")
        self.client.post(
            reverse("student:ide_submit"),
            data=json.dumps({"code": "fixed", "tests_passed": 3, "tests_total": 3}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {IdeToken.issue(self.student, self.bug, a)}",
        )
        submission = Submission.objects.get(student=self.student, assignment=a)
        self.assertIsNone(submission.tests_passed)
        self.assertIsNone(submission.tests_total)


class BridgeTests(TestCase):
    """core/bridge.py: VS Code containers reach the development server."""

    def test_server_url_follows_the_running_port(self):
        from core.bridge import ide_server_url

        with patch.dict("os.environ", {}, clear=False):
            os.environ.pop("DEBUG_GYM_IDE_SERVER_URL", None)
            self.assertEqual(ide_server_url(8000), "http://host.docker.internal:8000")

    @override_settings(DEBUG_GYM_IDE_SERVER_URL="https://gym.example.org")
    def test_explicit_setting_wins(self):
        from core.bridge import ide_server_url

        with patch.dict("os.environ", {"DEBUG_GYM_IDE_SERVER_URL": "https://gym.example.org"}):
            self.assertEqual(ide_server_url(8000), "https://gym.example.org")

    def test_runserver_port_parsing(self):
        from core.bridge import runserver_port

        self.assertEqual(runserver_port(["manage.py", "runserver"]), 8000)
        self.assertEqual(runserver_port(["manage.py", "runserver", "8001"]), 8001)
        self.assertEqual(runserver_port(["manage.py", "runserver", "127.0.0.1:8002", "--noreload"]), 8002)
        self.assertEqual(runserver_port(["manage.py", "runserver", "--noreload"]), 8000)

    def test_relay_only_for_servers_on_localhost(self):
        """On 0.0.0.0 the server is reachable already; a relay would block its own bind."""
        from core.bridge import runserver_address, start_with_runserver

        self.assertEqual(runserver_address(["manage.py", "runserver"]), ("127.0.0.1", 8000))
        self.assertEqual(runserver_address(["manage.py", "runserver", "0.0.0.0:8000"]), ("0.0.0.0", 8000))
        self.assertEqual(runserver_address(["manage.py", "runserver", "8001"]), ("127.0.0.1", 8001))
        with patch("core.bridge.ensure_relay") as relay, patch.dict(os.environ, {"RUN_MAIN": "true"}):
            start_with_runserver(["manage.py", "runserver", "0.0.0.0:8000"])
            start_with_runserver(["manage.py", "runserver", "172.17.0.1:8000"])
            relay.assert_not_called()
            start_with_runserver(["manage.py", "runserver", "127.0.0.1:8000"])
            for thread in threading.enumerate():
                if thread.name.startswith("Thread") and thread is not threading.current_thread():
                    thread.join(timeout=2)
            relay.assert_called_once_with(8000)

    def test_no_relay_outside_development(self):
        from core.bridge import ensure_relay

        with override_settings(DEBUG=False):
            self.assertFalse(ensure_relay(8000, address="127.0.0.2"))

    def test_relay_forwards_to_the_local_server(self):
        """A server on 127.0.0.1 answers through the relay on another local address."""
        import socket
        import threading
        import urllib.request
        from http.server import BaseHTTPRequestHandler, HTTPServer

        from core.bridge import ensure_relay

        class Hello(BaseHTTPRequestHandler):
            def do_POST(self):
                body = self.rfile.read(int(self.headers["Content-Length"]))
                self.send_response(201)
                self.end_headers()
                self.wfile.write(b"got " + body)

            def log_message(self, *args):
                pass

        server = HTTPServer(("127.0.0.1", 0), Hello)
        port = server.server_address[1]
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.shutdown)
        probe = socket.socket()
        try:
            probe.bind(("127.0.0.2", 0))
        except OSError:
            self.skipTest("127.0.0.2 is not available on this machine")
        finally:
            probe.close()

        with override_settings(DEBUG=True):
            self.assertTrue(ensure_relay(port, address="127.0.0.2"))
            self.assertTrue(ensure_relay(port, address="127.0.0.2"))  # second call reuses it
        with urllib.request.urlopen(urllib.request.Request(
            f"http://127.0.0.2:{port}/", data=b"fix", method="POST"), timeout=5) as response:
            self.assertEqual(response.status, 201)
            self.assertEqual(response.read(), b"got fix")
