import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch

from app.server import CatalogHandler, find_exercise, workspace_health_error


class WorkspaceHealthHandler(BaseHTTPRequestHandler):
    status = 200

    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        self.send_response(self.status)
        self.end_headers()

    def log_message(self, message_format: str, *args: object) -> None:
        pass


class FindExerciseTests(unittest.TestCase):
    def test_matches_supported_plain_language_request(self) -> None:
        exercise = find_exercise("I want a Python list mutation bug")

        self.assertIsNotNone(exercise)
        self.assertEqual(exercise["id"], "remove-negatives")

    def test_rejects_unsupported_bug_type(self) -> None:
        self.assertIsNone(find_exercise("A Python concurrency race condition"))

    def test_requires_python(self) -> None:
        self.assertIsNone(find_exercise("A Java list mutation bug"))


class WorkspaceHealthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = ThreadingHTTPServer(
            ("127.0.0.1", 0), WorkspaceHealthHandler
        )
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_health_check_accepts_ready_workspace(self) -> None:
        WorkspaceHealthHandler.status = 200

        self.assertIsNone(workspace_health_error(self.url))

    def test_health_check_reports_unavailable_workspace(self) -> None:
        WorkspaceHealthHandler.status = 503

        self.assertEqual(
            workspace_health_error(self.url),
            "The exercise workspace returned HTTP 503.",
        )


class CatalogApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), CatalogHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = f"http://127.0.0.1:{cls.server.server_port}/api/exercises"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def request(self, query: str) -> tuple[int, dict[str, object]]:
        request = urllib.request.Request(
            self.url,
            data=json.dumps({"query": query}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request) as response:
                return response.status, json.load(response)
        except urllib.error.HTTPError as error:
            return error.code, json.load(error)

    @patch("app.server.workspace_health_error", return_value=None)
    def test_supported_request_returns_workspace(self, _health_check: object) -> None:
        status, payload = self.request("A Python loop bug")

        self.assertEqual(status, 200)
        self.assertIn("workspaceUrl", payload["exercise"])

    @patch(
        "app.server.workspace_health_error",
        return_value="The exercise workspace is unavailable. Please try again shortly.",
    )
    def test_supported_request_reports_unavailable_workspace(
        self, _health_check: object
    ) -> None:
        status, payload = self.request("A Python loop bug")

        self.assertEqual(status, 503)
        self.assertIn("workspace is unavailable", payload["error"])

    def test_unsupported_request_does_not_create_workspace(self) -> None:
        status, payload = self.request("A Python concurrency bug")

        self.assertEqual(status, 404)
        self.assertIn("No prepared exercise", payload["error"])


if __name__ == "__main__":
    unittest.main()
