import importlib.util
import json
import re
from pathlib import Path
from unittest.mock import patch

from django.test import TestCase, override_settings

from bugs.tests import make_user
from config import analytics

REPO = Path(__file__).resolve().parents[3]
URL = "https://analytics.example.test/events"


def emitted(mock):
    return [(call.args[0], call.kwargs) for call in mock.call_args_list]


class CatalogEventTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client.force_login(self.user)

    @patch("bugs.views.emit")
    def test_search_records_the_result_count(self, emit):
        response = self.client.post(
            "/api/exercises", data={"query": "remove negatives"}, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        count = len(response.json()["exercises"])
        self.assertEqual(emitted(emit), [("exercise_searched", {"result_count": count})])

    @patch("bugs.views.emit")
    def test_search_without_a_match_records_zero(self, emit):
        response = self.client.post(
            "/api/exercises", data={"query": "zzzqqq"}, content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(emitted(emit), [("exercise_searched", {"result_count": 0})])

    @patch("bugs.views.emit")
    def test_a_rejected_query_records_nothing(self, emit):
        self.client.post("/api/exercises", data={"query": 5}, content_type="application/json")
        emit.assert_not_called()

    @patch("bugs.views.emit")
    def test_opening_an_exercise_records_its_slug(self, emit):
        self.assertEqual(self.client.get("/api/bugs/remove-negatives/").status_code, 200)
        self.assertEqual(emitted(emit), [("exercise_opened", {"exercise_slug": "remove-negatives"})])

    @patch("bugs.views.emit")
    def test_an_exercise_that_is_not_visible_records_nothing(self, emit):
        self.assertEqual(self.client.get("/api/bugs/missing/").status_code, 404)
        emit.assert_not_called()

    @patch("bugs.views.emit")
    def test_a_signed_out_request_records_nothing(self, emit):
        self.client.logout()
        self.client.get("/api/bugs/remove-negatives/")
        emit.assert_not_called()


class WorkspaceEventTests(TestCase):
    url = "/api/bugs/remove-negatives/vscode/"

    def setUp(self):
        self.client.force_login(make_user())

    @patch("bugs.views.emit")
    @patch("bugs.workspaces.write_workspace", return_value="folder")
    @patch("bugs.ide.start_ide", return_value=49153)
    def test_opening_the_workspace_records_the_event(self, _start, _write, emit):
        self.assertEqual(self.client.post(self.url).status_code, 200)
        self.assertEqual(emitted(emit), [("workspace_opened", {"exercise_slug": "remove-negatives"})])

    @patch("bugs.views.emit")
    @patch("bugs.workspaces.write_workspace", return_value="folder")
    @patch("bugs.ide.start_ide")
    def test_a_workspace_that_did_not_start_records_nothing(self, start, _write, emit):
        from bugs.ide import IdeError

        start.side_effect = IdeError("no docker")
        self.assertEqual(self.client.post(self.url).status_code, 503)
        emit.assert_not_called()


class VerificationEventTests(TestCase):
    url = "/api/bugs/remove-negatives/attempts/"

    def setUp(self):
        self.client.force_login(make_user())

    def submit(self, claimed_passed=3, claimed_total=3):
        return self.client.post(
            self.url,
            data={"code": "x = 1\n", "passed": claimed_passed, "total": claimed_total},
            content_type="application/json",
        )

    @patch("bugs.views.emit")
    @patch("bugs.verification.verify_submission", return_value=(3, 3))
    def test_a_passing_run_records_all_passed(self, _verify, emit):
        self.assertEqual(self.submit().status_code, 201)
        self.assertEqual(
            emitted(emit),
            [("solution_verified", {
                "exercise_slug": "remove-negatives", "passed_count": 3, "total_count": 3, "all_passed": True,
            })],
        )

    @patch("bugs.views.emit")
    @patch("bugs.verification.verify_submission", return_value=(1, 3))
    def test_counts_come_from_the_container_not_the_client(self, _verify, emit):
        self.assertEqual(self.submit(claimed_passed=3, claimed_total=3).status_code, 201)
        (_, fields), = emitted(emit)
        self.assertEqual((fields["passed_count"], fields["total_count"], fields["all_passed"]), (1, 3, False))

    @patch("bugs.views.emit")
    @patch("bugs.verification.verify_submission", return_value=(0, 0))
    def test_a_run_with_no_tests_is_not_all_passed(self, _verify, emit):
        self.submit()
        (_, fields), = emitted(emit)
        self.assertIs(fields["all_passed"], False)

    @patch("bugs.views.emit")
    @patch("bugs.verification.verify_submission")
    def test_a_run_that_could_not_verify_records_nothing(self, verify, emit):
        from bugs.verification import VerificationBusy

        verify.side_effect = VerificationBusy("busy")
        self.assertEqual(self.submit().status_code, 503)
        emit.assert_not_called()

    @patch("bugs.views.emit")
    def test_an_invalid_body_records_nothing(self, emit):
        response = self.client.post(self.url, data={"code": 5}, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        emit.assert_not_called()


@override_settings(DEBUG_GYM_ANALYTICS_URL=URL, DEBUG_GYM_ANALYTICS_KEY="k")
class EndToEndEventTests(TestCase):
    """A real emit() through a view: the right payload is queued, and a dead backend is harmless."""

    def setUp(self):
        self.user = make_user()
        self.client.force_login(self.user)

    @patch("config.analytics._ensure_worker")
    def test_the_view_queues_a_valid_event(self, _worker):
        while not analytics._queue.empty():
            analytics._queue.get_nowait()
        self.assertEqual(self.client.get("/api/bugs/remove-negatives/").status_code, 200)
        _url, _key, event = analytics._queue.get_nowait()
        self.assertEqual(event["name"], "exercise_opened")
        self.assertEqual(event["source"], "web")
        self.assertEqual(event["learner_id"], analytics.learner_id(self.user))
        self.assertNotIn(self.user.email, str(event))

    @patch("config.analytics._post", side_effect=OSError("backend down"))
    def test_a_dead_backend_does_not_break_the_request(self, _post):
        with self.assertLogs("debug_gym.analytics", "WARNING"):
            response = self.client.get("/api/bugs/remove-negatives/")
            analytics.flush()
        self.assertEqual(response.status_code, 200)


class SmokeScriptTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        spec = importlib.util.spec_from_file_location("send_smoke_event", REPO / "scripts" / "send_smoke_event.py")
        cls.script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.script)

    def test_every_registry_event_is_sent_with_exactly_its_fields(self):
        events = self.script.smoke_events()
        self.assertEqual({e["name"] for e in events}, set(analytics.EVENTS))
        for event in events:
            schema = analytics.EVENTS[event["name"]]
            body = set(event) - {"name", "timestamp", "learner_id", "source"}
            self.assertEqual(body, set(schema), event["name"])
            for field, expected in schema.items():
                self.assertIs(type(event[field]), expected, f"{event['name']}.{field}")

    def test_every_event_is_tagged_smoke_and_has_no_personal_data(self):
        for event in self.script.smoke_events():
            self.assertEqual(event["source"], "smoke")
            self.assertEqual(len(event["learner_id"]), 32)
            self.assertNotIn("@", json.dumps(event))

    def test_a_url_that_is_not_https_is_refused(self):
        self.assertEqual(self.script.main(["--url", "http://analytics.example.test"]), 2)

    def test_a_dry_run_sends_nothing(self):
        with patch.object(self.script, "send") as send:
            self.assertEqual(self.script.main(["--url", URL, "--dry-run"]), 0)
        send.assert_not_called()


class MetricQueriesExcludeSmokeTests(TestCase):
    def test_every_query_in_the_analytics_plan_excludes_smoke_events(self):
        plan = REPO / "docs" / "analytics.md"
        if not plan.exists():
            self.skipTest("docs/analytics.md is not part of this checkout")
        queries = re.findall(r"```sql\n(.*?)```", plan.read_text(encoding="utf-8"), re.S)
        self.assertTrue(queries, "the plan has no SQL queries to check")
        for query in queries:
            self.assertRegex(query, r"source\s*(=\s*'web'|(<>|!=)\s*'smoke')", query[:60])
