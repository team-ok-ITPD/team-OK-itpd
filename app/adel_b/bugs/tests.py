import json
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest import mock

import docker
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.staticfiles import finders
from django.test import Client, TestCase, override_settings

from . import ide
from .ide import IdeError, start_ide
from .models import Attempt, Bug, Draft, IdeToken
from .workspaces import WorkspaceError, render_tests, write_workspace


def make_user(username="learner", **extra):
    return get_user_model().objects.create_user(
        username=username, email=f"{username}@example.com", password="debug-gym-pass", **extra
    )


class BugApiTests(TestCase):
    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_page_exercises_are_seeded(self):
        response = self.client.get("/api/bugs/")
        self.assertEqual(response.status_code, 200)
        ids = [bug["id"] for bug in response.json()["bugs"]]
        self.assertEqual(
            ids,
            [
                "remove-negatives",
                "total-starts-late",
                "duplicated-result",
                "missing-last-element",
                "count-words",
            ],
        )

    def test_only_workspace_bugs_have_a_workspace_url(self):
        bugs = {bug["id"]: bug for bug in self.client.get("/api/bugs/").json()["bugs"]}
        self.assertEqual(bugs["remove-negatives"]["workspaceUrl"], "http://localhost:8080")
        self.assertIsNone(bugs["count-words"]["workspaceUrl"])

    def test_bug_detail(self):
        response = self.client.get("/api/bugs/remove-negatives/")
        self.assertEqual(response.status_code, 200)
        bug = response.json()["bug"]
        self.assertEqual(bug["title"], "The surviving negative")
        self.assertIn("numbers.remove(number)", bug["buggyCode"])

    def test_unknown_bug_returns_404(self):
        response = self.client.get("/api/bugs/missing/")
        self.assertEqual(response.status_code, 404)

    def test_create_bug_needs_staff(self):
        self.client.force_login(make_user())
        response = self.client.post(
            "/api/bugs/",
            data=json.dumps({"slug": "x", "title": "X", "description": "X"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_create_bug(self):
        self.client.force_login(make_user(is_staff=True))
        response = self.client.post(
            "/api/bugs/",
            data=json.dumps({
                "slug": "off-by-one",
                "title": "One step too far",
                "description": "A loop reads past the end of the list.",
                "topic": "Indexes",
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["bug"]["id"], "off-by-one")
        self.assertTrue(Bug.objects.filter(slug="off-by-one").exists())

    def test_create_rejects_missing_fields(self):
        self.client.force_login(make_user(is_staff=True))
        response = self.client.post(
            "/api/bugs/", data=json.dumps({"slug": "x"}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_create_rejects_duplicate_slug(self):
        self.client.force_login(make_user(is_staff=True))
        response = self.client.post(
            "/api/bugs/",
            data=json.dumps({
                "slug": "remove-negatives",
                "title": "Again",
                "description": "Duplicate.",
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 409)

    def test_create_rejects_bad_json(self):
        self.client.force_login(make_user(is_staff=True))
        response = self.client.post(
            "/api/bugs/", data="not json", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)


class PageAndMatchTests(TestCase):
    def test_index_page_loads_the_two_screens(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="view-new"')
        self.assertContains(response, 'id="view-practice"')
        self.assertContains(response, "/static/bugs/app.js")

    def test_practice_is_a_results_view_without_a_browser_editor(self):
        response = self.client.get("/")
        for element in ("reproduce-title", "test-list", "console-output", "run-tests", "submit", "workspace"):
            self.assertContains(response, f'id="{element}"')
        for removed in ("code-input", "reset-code", "console-form", "console-command"):
            self.assertNotContains(response, f'id="{removed}"')

    def test_page_assets_are_found(self):
        self.assertIsNotNone(finders.find("bugs/app.js"))
        self.assertIsNotNone(finders.find("bugs/styles.css"))

    def test_match_list_mutation_query(self):
        response = self.client.post(
            "/api/exercises",
            data=json.dumps({"query": "A Python list mutation bug with negative numbers"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["exercise"]["id"], "remove-negatives")

    def search(self, query):
        response = self.client.post(
            "/api/exercises", data=json.dumps({"query": query}), content_type="application/json"
        )
        body = response.json()
        return [exercise["id"] for exercise in body.get("exercises", [])], body.get("matchedBy")

    def test_match_by_title_lists_every_matching_title(self):
        self.assertEqual(self.search("duplicate"), (["duplicated-result", "count-words"], "title"))

    def test_match_title_by_word_start(self):
        self.assertEqual(self.search("dict"), (["count-words"], "title"))
        self.assertEqual(self.search("missing element"), (["missing-last-element"], "title"))

    def test_more_matching_title_words_rank_higher(self):
        ids, matched_by = self.search("duplicate dictionary")
        self.assertEqual((ids[0], matched_by), ("count-words", "title"))

    def test_best_match_is_also_returned_alone(self):
        response = self.client.post(
            "/api/exercises", data=json.dumps({"query": "surviving negative"}), content_type="application/json"
        )
        self.assertEqual(response.json()["exercise"]["id"], "remove-negatives")

    def test_falls_back_to_descriptions_when_no_title_matches(self):
        self.assertEqual(
            self.search("sum of scores"), (["total-starts-late", "missing-last-element"], "description")
        )

    def test_asset_links_change_with_the_files(self):
        response = self.client.get("/")
        self.assertRegex(response.content.decode(), r"bugs/app\.js\?v=\d+")

    def test_match_dictionary_query(self):
        response = self.client.post(
            "/api/exercises",
            data=json.dumps({"query": "counting words in a dictionary"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["exercise"]["id"], "count-words")

    def test_match_unknown_query_returns_404(self):
        response = self.client.post(
            "/api/exercises",
            data=json.dumps({"query": "javascript promise deadlock"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)

    def test_match_rejects_non_text_query(self):
        response = self.client.post(
            "/api/exercises", data=json.dumps({"query": 5}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)


class DraftApiTests(TestCase):
    url = "/api/bugs/remove-negatives/draft/"

    def setUp(self):
        self.client.force_login(make_user())

    def test_needs_login(self):
        self.client.logout()
        self.assertEqual(self.client.get(self.url).status_code, 401)

    def test_drafts_are_private(self):
        self.put({"code": "mine\n"})
        self.client.force_login(make_user("other"))
        self.assertIsNone(self.client.get(self.url).json()["draft"])

    def put(self, payload):
        return self.client.put(self.url, data=json.dumps(payload), content_type="application/json")

    def test_no_draft_at_first(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json()["draft"])

    def test_save_and_load_draft(self):
        code = "def remove_negatives(numbers):\n    return [n for n in numbers if n >= 0]\n"
        self.assertEqual(self.put({"code": code}).status_code, 200)
        self.assertEqual(self.put({"code": code + "# again\n"}).status_code, 200)
        self.assertEqual(Draft.objects.count(), 1)
        draft = self.client.get(self.url).json()["draft"]
        self.assertEqual(draft["code"], code + "# again\n")
        self.assertEqual(draft["bugId"], "remove-negatives")

    def test_delete_resets_draft(self):
        self.put({"code": "pass\n"})
        self.assertEqual(self.client.delete(self.url).status_code, 200)
        self.assertIsNone(self.client.get(self.url).json()["draft"])

    def test_rejects_non_text_code(self):
        self.assertEqual(self.put({"code": 5}).status_code, 400)

    def test_rejects_huge_code(self):
        self.assertEqual(self.put({"code": "x" * 50_001}).status_code, 400)

    def test_unknown_bug_returns_404(self):
        response = self.client.get("/api/bugs/missing/draft/")
        self.assertEqual(response.status_code, 404)


class AttemptAndHistoryTests(TestCase):
    url = "/api/bugs/remove-negatives/attempts/"

    def setUp(self):
        self.client.force_login(make_user())

    def test_needs_login(self):
        self.client.logout()
        self.assertEqual(self.submit(3).status_code, 401)
        self.assertEqual(self.client.get("/api/history/").status_code, 401)

    def test_history_is_private(self):
        self.submit(3)
        self.client.force_login(make_user("other"))
        self.assertEqual(self.client.get("/api/history/").json(), {"items": [], "activity": []})
        self.assertEqual(self.client.get(self.url).json(), {"attempts": []})

    def submit(self, passed, total=3, code="def remove_negatives(numbers):\n    return numbers\n"):
        return self.client.post(
            self.url,
            data=json.dumps({"code": code, "passed": passed, "total": total}),
            content_type="application/json",
        )

    def test_failed_attempt_is_saved(self):
        response = self.submit(1)
        self.assertEqual(response.status_code, 201)
        attempt = response.json()["attempt"]
        self.assertEqual((attempt["passed"], attempt["total"], attempt["solved"]), (1, 3, False))
        self.assertEqual(Attempt.objects.count(), 1)

    def test_passing_attempt_is_solved(self):
        self.assertTrue(self.submit(3).json()["attempt"]["solved"])

    def test_list_attempts_newest_first(self):
        self.submit(1)
        self.submit(3)
        attempts = self.client.get(self.url).json()["attempts"]
        self.assertEqual([attempt["passed"] for attempt in attempts], [3, 1])

    def test_rejects_wrong_test_count(self):
        self.assertEqual(self.submit(2, total=2).status_code, 400)

    def test_rejects_passed_above_total(self):
        self.assertEqual(self.submit(4).status_code, 400)

    def test_rejects_non_integer_counts(self):
        self.assertEqual(self.submit("3").status_code, 400)
        self.assertEqual(self.submit(True).status_code, 400)

    def test_unknown_bug_returns_404(self):
        response = self.client.post(
            "/api/bugs/missing/attempts/",
            data=json.dumps({"code": "", "passed": 0, "total": 0}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)

    def test_history_is_empty_at_first(self):
        self.assertEqual(self.client.get("/api/history/").json(), {"items": [], "activity": []})

    def test_history_statuses(self):
        self.client.put(
            "/api/bugs/count-words/draft/",
            data=json.dumps({"code": "pass\n"}),
            content_type="application/json",
        )
        self.submit(1)
        self.client.post(
            "/api/bugs/total-starts-late/attempts/",
            data=json.dumps({"code": "", "passed": 3, "total": 3}),
            content_type="application/json",
        )
        body = self.client.get("/api/history/").json()
        statuses = {item["bugId"]: item["status"] for item in body["items"]}
        self.assertEqual(
            statuses,
            {"count-words": "progress", "remove-negatives": "failed", "total-starts-late": "solved"},
        )
        self.assertEqual(body["items"][0]["bugId"], "total-starts-late")
        self.assertEqual(len(body["activity"]), 2)

    def test_one_solve_keeps_bug_solved(self):
        self.submit(3)
        self.submit(1)
        items = self.client.get("/api/history/").json()["items"]
        self.assertEqual(items[0]["status"], "solved")


class CsrfTests(TestCase):
    def test_changes_need_the_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(make_user())
        url = "/api/bugs/remove-negatives/draft/"
        body = json.dumps({"code": "pass\n"})
        self.assertEqual(client.put(url, data=body, content_type="application/json").status_code, 403)

        client.get("/")  # the page hands out the CSRF cookie
        token = client.cookies["csrftoken"].value
        response = client.put(url, data=body, content_type="application/json", HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, 200)


class TestEditTests(TestCase):
    url = "/api/bugs/remove-negatives/tests/1/"

    def setUp(self):
        self.client.force_login(make_user())

    def edit(self, input_text, expected_text, url=None):
        return self.client.put(
            url or self.url,
            data=json.dumps({"input": input_text, "expected": expected_text}),
            content_type="application/json",
        )

    def draft(self):
        return self.client.get("/api/bugs/remove-negatives/draft/").json()["draft"]

    def test_edit_one_test(self):
        response = self.edit("[7, -1, -2]", "[7]")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body["edited"])
        self.assertEqual(body["tests"][1], {"name": "Mixed numbers", "input": [7, -1, -2], "expected": [7]})
        self.assertEqual(body["tests"][0]["input"], [])
        self.assertEqual(self.draft()["tests"], body["tests"])
        self.assertEqual(Bug.objects.get(slug="remove-negatives").tests[1]["input"], [4, -3, -2, 5])

    def test_python_values_are_read_safely(self):
        response = self.edit("{'apple': 2, 'pear': None}", "'it\\'s'", url="/api/bugs/count-words/tests/0/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["tests"][0]["input"], {"apple": 2, "pear": None})
        self.assertEqual(response.json()["tests"][0]["expected"], "it's")

    def test_rejects_code_and_unsupported_values(self):
        for bad in ("__import__('os')", "[1, 2", "(1, 2)", "{1: 2}", "", "1e999", "x" * 2001):
            response = self.edit(bad, "[]")
            self.assertEqual(response.status_code, 400, bad)
            self.assertIn("input", response.json()["fields"])
        self.assertIsNone(self.draft())

    def test_restore_original(self):
        self.edit("[7, -1]", "[7]")
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["edited"])
        self.assertIsNone(self.draft()["tests"])

    def test_saving_the_original_values_is_not_an_edit(self):
        response = self.edit("[4, -3, -2, 5]", "[4, 5]")
        self.assertFalse(response.json()["edited"])
        self.assertIsNone(self.draft())

    def test_unknown_test_returns_404(self):
        self.assertEqual(self.edit("[]", "[]", url="/api/bugs/remove-negatives/tests/3/").status_code, 404)

    def test_needs_login(self):
        self.client.logout()
        self.assertEqual(self.edit("[]", "[]").status_code, 401)

    def test_code_edits_keep_edited_tests(self):
        self.edit("[7, -1]", "[7]")
        self.client.put(
            "/api/bugs/remove-negatives/draft/",
            data=json.dumps({"code": "changed\n"}),
            content_type="application/json",
        )
        self.assertEqual(self.draft()["tests"][1]["input"], [7, -1])

    def test_reset_code_keeps_edited_tests(self):
        self.client.put(
            "/api/bugs/remove-negatives/draft/",
            data=json.dumps({"code": "changed\n"}),
            content_type="application/json",
        )
        self.edit("[7, -1]", "[7]")
        response = self.client.delete("/api/bugs/remove-negatives/draft/")
        draft = response.json()["draft"]
        self.assertIn("numbers.remove(number)", draft["code"])
        self.assertEqual(draft["tests"][1]["input"], [7, -1])


class WorkspaceFilesTests(TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        override = override_settings(WORKSPACES_DIR=Path(self.tmp.name))
        override.enable()
        self.addCleanup(override.disable)
        self.user = make_user()
        self.bug = Bug.objects.get(slug="remove-negatives")

    def run_pytest(self, folder):
        return subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"],
            cwd=folder,
            capture_output=True,
            text=True,
            timeout=60,
        )

    def test_writes_code_tests_and_launch_config(self):
        folder = write_workspace(self.user, self.bug)
        self.assertEqual(folder, Path(self.tmp.name) / str(self.user.id) / "remove-negatives")
        self.assertEqual((folder / "remove_negatives.py").read_text(), self.bug.buggy_code + "\n")
        exercise_launch = json.loads(
            (settings.BASE_DIR.parent.parent / "exercise" / ".vscode" / "launch.json").read_text()
        )
        launch = json.loads((folder / ".vscode" / "launch.json").read_text())
        for configuration in exercise_launch["configurations"]:
            configuration["python"] = "/opt/debug-gym/bin/python"
        self.assertEqual(launch, exercise_launch)
        self.assertEqual(launch["configurations"][0]["module"], "pytest")
        self.assertEqual(
            json.loads((folder / ".vscode" / "settings.json").read_text()),
            {"python.defaultInterpreterPath": "/opt/debug-gym/bin/python"},
        )
        tests = (folder / "tests" / "test_remove_negatives.py").read_text()
        self.assertIn("from remove_negatives import remove_negatives", tests)
        self.assertIn("def test_mixed_numbers() -> None:", tests)
        self.assertIn("assert remove_negatives([4, -3, -2, 5]) == [4, 5]", tests)

    def test_generated_tests_fail_on_the_buggy_code(self):
        result = self.run_pytest(write_workspace(self.user, self.bug))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("2 failed, 1 passed", result.stdout)

    def test_uses_the_learners_draft_and_passes_when_fixed(self):
        fixed = "def remove_negatives(numbers):\n    return [n for n in numbers if n >= 0]\n"
        Draft.objects.create(user=self.user, bug=self.bug, code=fixed)
        folder = write_workspace(self.user, self.bug)
        self.assertEqual((folder / "remove_negatives.py").read_text(), fixed)
        result = self.run_pytest(folder)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("3 passed", result.stdout)

    def test_dictionary_bug_tests(self):
        bug = Bug.objects.get(slug="count-words")
        result = self.run_pytest(write_workspace(self.user, bug))
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("FAILED tests/test_count_words.py::test_mixed_case", result.stdout)
        self.assertIn("1 failed, 2 passed", result.stdout)

    def test_each_user_gets_their_own_folder(self):
        other = make_user("other")
        self.assertNotEqual(write_workspace(self.user, self.bug), write_workspace(other, self.bug))

    def test_rejects_unsafe_names(self):
        for field, value in (("file_name", "../evil.py"), ("function_name", "x; import os")):
            bug = Bug.objects.get(slug="remove-negatives")
            setattr(bug, field, value)
            with self.assertRaises(WorkspaceError):
                write_workspace(self.user, bug)

    def test_rejects_non_literal_test_values(self):
        self.bug.tests = [{"name": "Bad", "input": object(), "expected": []}]
        with self.assertRaises(WorkspaceError):
            render_tests(self.bug)

    def test_duplicate_test_names_get_unique_functions(self):
        self.bug.tests = [
            {"name": "Same", "input": [], "expected": []},
            {"name": "Same", "input": [1], "expected": [1]},
        ]
        source = render_tests(self.bug)
        self.assertIn("def test_same() -> None:", source)
        self.assertIn("def test_same_2() -> None:", source)


class StartIdeTests(TestCase):
    folder = Path("/srv/workspaces/1/remove-negatives")

    def setUp(self):
        self.user = make_user()
        self.client_mock = mock.MagicMock()
        patcher = mock.patch("bugs.ide.docker.from_env", return_value=self.client_mock)
        patcher.start()
        self.addCleanup(patcher.stop)
        ready = mock.patch("bugs.ide._wait_until_ready")
        self.wait = ready.start()
        self.addCleanup(ready.stop)

    def container(self, status="running", folder=None, port="49153", image=None, command=None):
        command = command or ide.settings_label()
        container = mock.MagicMock()
        container.status = status
        container.labels = {"debug-gym.folder": str(folder or self.folder), "debug-gym.settings": command}
        container.ports = {"8080/tcp": [{"HostIp": "127.0.0.1", "HostPort": port}]}
        container.image.id = image or self.client_mock.images.get.return_value.id
        return container

    def test_starts_a_new_container(self):
        self.client_mock.containers.get.side_effect = docker.errors.NotFound("missing")
        self.client_mock.containers.run.return_value = self.container(port="49200")
        self.assertEqual(start_ide(self.user, self.folder), 49200)
        args, kwargs = self.client_mock.containers.run.call_args
        self.assertEqual(args, ("debug-gym-ide",))
        self.assertEqual(kwargs["name"], f"debug-gym-ide-{self.user.id}")
        self.assertEqual(kwargs["entrypoint"], ["code-server"])
        self.assertEqual(
            kwargs["command"][:2] + kwargs["command"][-1:], ["--auth", "none", "/home/coder/project"]
        )
        self.assertIn("/opt/debug-gym/extensions", kwargs["command"])
        self.assertEqual(kwargs["volumes"], {str(self.folder): {"bind": "/home/coder/project", "mode": "rw"}})
        self.assertEqual(kwargs["ports"], {"8080/tcp": ("127.0.0.1", None)})
        self.assertEqual(kwargs["mem_limit"], "512m")
        self.assertEqual(kwargs["security_opt"], ["no-new-privileges:true"])
        self.assertTrue(kwargs["environment"]["PATH"].startswith("/opt/debug-gym/bin:"))
        self.assertEqual(kwargs["extra_hosts"], {"host.docker.internal": "host-gateway"})
        self.assertIn("--disable-workspace-trust", kwargs["command"])
        self.assertIn("--disable-proxy", kwargs["command"])
        self.wait.assert_called_once_with(49200)

    def test_reuses_a_running_container_for_the_same_bug(self):
        existing = self.container(port="49300")
        self.client_mock.containers.get.return_value = existing
        self.assertEqual(start_ide(self.user, self.folder), 49300)
        self.client_mock.containers.run.assert_not_called()
        existing.remove.assert_not_called()

    def test_replaces_the_container_for_another_bug(self):
        existing = self.container(folder="/srv/workspaces/1/count-words")
        self.client_mock.containers.get.return_value = existing
        self.client_mock.containers.run.return_value = self.container(port="49400")
        self.assertEqual(start_ide(self.user, self.folder), 49400)
        existing.remove.assert_called_once_with(force=True)
        self.client_mock.containers.run.assert_called_once()

    def test_replaces_a_container_from_an_older_image(self):
        existing = self.container(image="sha256:old")
        self.client_mock.containers.get.return_value = existing
        self.client_mock.containers.run.return_value = self.container(port="49600")
        self.assertEqual(start_ide(self.user, self.folder), 49600)
        existing.remove.assert_called_once_with(force=True)

    def test_replaces_a_container_started_with_older_settings(self):
        existing = self.container(command="0000000000000000")
        self.client_mock.containers.get.return_value = existing
        self.client_mock.containers.run.return_value = self.container(port="49700")
        self.assertEqual(start_ide(self.user, self.folder), 49700)
        existing.remove.assert_called_once_with(force=True)

    def test_replaces_a_stopped_container(self):
        existing = self.container(status="exited")
        self.client_mock.containers.get.return_value = existing
        self.client_mock.containers.run.return_value = self.container(port="49500")
        self.assertEqual(start_ide(self.user, self.folder), 49500)
        existing.remove.assert_called_once_with(force=True)

    def test_docker_not_running(self):
        with mock.patch("bugs.ide.docker.from_env", side_effect=docker.errors.DockerException("no socket")):
            with self.assertRaisesRegex(IdeError, "Docker is not running"):
                start_ide(self.user, self.folder)

    def test_image_not_built(self):
        self.client_mock.containers.get.side_effect = docker.errors.NotFound("missing")
        self.client_mock.containers.run.side_effect = docker.errors.ImageNotFound("no image")
        with self.assertRaisesRegex(IdeError, "is not built"):
            start_ide(self.user, self.folder)


class WaitUntilReadyTests(TestCase):
    def test_gives_up_when_vs_code_never_answers(self):
        with mock.patch("bugs.ide.READY_TIMEOUT_SECONDS", 0):
            with self.assertRaisesRegex(IdeError, "did not start in time"):
                ide._wait_until_ready(1)

    def test_returns_once_healthz_answers(self):
        response = mock.MagicMock(status=200)
        response.__enter__.return_value = response
        with mock.patch("bugs.ide.urlopen", return_value=response) as urlopen:
            ide._wait_until_ready(49153)
        urlopen.assert_called_once_with("http://127.0.0.1:49153/healthz", timeout=2)


class VscodeEndpointTests(TestCase):
    url = "/api/bugs/remove-negatives/vscode/"

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        override = override_settings(WORKSPACES_DIR=Path(self.tmp.name))
        override.enable()
        self.addCleanup(override.disable)
        self.user = make_user()
        self.client.force_login(self.user)

    def test_writes_the_workspace_and_returns_the_vs_code_url(self):
        with mock.patch("bugs.ide.start_ide", return_value=49153) as start:
            response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"url": "http://localhost:49153/?folder=/home/coder/project"})
        folder = Path(self.tmp.name) / str(self.user.id) / "remove-negatives"
        start.assert_called_once_with(self.user, folder)
        self.assertTrue((folder / "tests" / "test_remove_negatives.py").exists())

    def test_full_path_with_mocked_docker(self):
        docker_client = mock.MagicMock()
        docker_client.containers.get.side_effect = docker.errors.NotFound("missing")
        container = docker_client.containers.run.return_value
        container.ports = {"8080/tcp": [{"HostIp": "127.0.0.1", "HostPort": "49999"}]}
        with mock.patch("bugs.ide.docker.from_env", return_value=docker_client), mock.patch(
            "bugs.ide._wait_until_ready"
        ):
            response = self.client.post(self.url)
        self.assertEqual(response.json()["url"], "http://localhost:49999/?folder=/home/coder/project")
        folder = str(Path(self.tmp.name) / str(self.user.id) / "remove-negatives")
        self.assertIn(folder, docker_client.containers.run.call_args.kwargs["volumes"])

    def test_docker_not_running_is_a_clear_json_error(self):
        with mock.patch("bugs.ide.docker.from_env", side_effect=docker.errors.DockerException("no socket")):
            response = self.client.post(self.url)
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {"error": "Docker is not running on the server, so VS Code cannot start."})

    def test_needs_login(self):
        self.client.logout()
        with mock.patch("bugs.ide.start_ide") as start:
            self.assertEqual(self.client.post(self.url).status_code, 401)
        start.assert_not_called()

    def test_unknown_bug(self):
        self.assertEqual(self.client.post("/api/bugs/missing/vscode/").status_code, 404)

    def test_get_is_not_allowed(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_needs_the_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        with mock.patch("bugs.ide.start_ide") as start:
            self.assertEqual(client.post(self.url).status_code, 403)
        start.assert_not_called()


class IdeSubmitTests(TestCase):
    url = "/api/ide/submit/"

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        override = override_settings(WORKSPACES_DIR=Path(self.tmp.name))
        override.enable()
        self.addCleanup(override.disable)
        self.user = make_user()
        self.bug = Bug.objects.get(slug="remove-negatives")
        self.folder = write_workspace(self.user, self.bug)
        self.config = json.loads((self.folder / ".debug-gym" / "config.json").read_text())

    def submit(self, token=None, **payload):
        body = {"bug": "remove-negatives", "code": "def remove_negatives(n):\n    return n\n", "passed": 3, "total": 3}
        body.update(payload)
        headers = {} if token == "" else {"HTTP_AUTHORIZATION": f"Bearer {token or self.config['token']}"}
        return Client(enforce_csrf_checks=True).post(
            self.url, data=json.dumps(body), content_type="application/json", **headers
        )

    def test_config_file(self):
        self.assertEqual(
            {key: value for key, value in self.config.items() if key != "token"},
            {
                "server": "http://host.docker.internal:8001",
                "site": "http://localhost:8001/#/practice/remove-negatives",
                "bug": "remove-negatives",
                "file": "remove_negatives.py",
            },
        )
        self.assertGreaterEqual(len(self.config["token"]), 40)
        self.assertEqual((self.folder / ".debug-gym" / "config.json").stat().st_mode & 0o777, 0o600)

    def test_only_a_hash_of_the_token_is_stored(self):
        stored = IdeToken.objects.get(user=self.user, bug=self.bug)
        self.assertNotEqual(stored.key_hash, self.config["token"])
        self.assertEqual(IdeToken.find(self.config["token"]), stored)

    def test_submit_saves_an_attempt_for_the_tokens_user(self):
        response = self.submit()
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["attempt"]["solved"])
        attempt = Attempt.objects.get()
        self.assertEqual((attempt.user, attempt.bug, attempt.passed_count), (self.user, self.bug, 3))
        self.client.force_login(self.user)
        self.assertEqual(self.client.get("/api/history/").json()["items"][0]["status"], "solved")

    def test_submitted_code_becomes_the_website_draft(self):
        code = "def remove_negatives(n):\n    return [x for x in n if x >= 0]\n"
        self.submit(code=code)
        self.assertEqual(Draft.objects.get(user=self.user, bug=self.bug).code, code)
        self.assertEqual((write_workspace(self.user, self.bug) / "remove_negatives.py").read_text(), code)

    def test_rejected_submission_keeps_the_draft(self):
        Draft.objects.create(user=self.user, bug=self.bug, code="mine\n")
        self.submit(total=2, passed=2)
        self.assertEqual(Draft.objects.get(user=self.user, bug=self.bug).code, "mine\n")

    def test_failed_submission(self):
        response = self.submit(passed=1)
        self.assertEqual(response.status_code, 201)
        self.assertFalse(response.json()["attempt"]["solved"])

    def test_reopening_replaces_the_token(self):
        old = self.config["token"]
        write_workspace(self.user, self.bug)
        self.assertEqual(self.submit(token=old).status_code, 401)
        new = json.loads((self.folder / ".debug-gym" / "config.json").read_text())["token"]
        self.assertEqual(self.submit(token=new).status_code, 201)

    def test_rejects_missing_or_wrong_token(self):
        self.assertEqual(self.submit(token="").status_code, 401)
        self.assertEqual(self.submit(token="not-a-real-token").status_code, 401)
        self.assertFalse(Attempt.objects.exists())

    def test_token_only_works_for_its_bug(self):
        response = self.submit(bug="count-words")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Attempt.objects.exists())

    def test_same_checks_as_the_website(self):
        self.assertEqual(self.submit(total=2, passed=2).status_code, 400)
        self.assertEqual(self.submit(passed="3").status_code, 400)
        self.assertEqual(self.submit(code=None).status_code, 400)

    def test_containers_can_reach_the_server(self):
        self.assertIn("host.docker.internal", settings.ALLOWED_HOSTS)
