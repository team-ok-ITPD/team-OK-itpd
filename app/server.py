"""Serve the minimum Debug GYM exercise catalog without external packages."""

from __future__ import annotations

import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


STATIC_DIR = Path(__file__).with_name("static")
SUPPORTED_TERMS = {
    "array",
    "arrays",
    "list",
    "lists",
    "loop",
    "loops",
    "mutation",
    "negative",
    "negatives",
}


def find_exercise(query: str) -> dict[str, Any] | None:
    """Return the curated exercise when a query describes its bug category."""
    words = {word.strip(".,!?;:").lower() for word in query.split()}
    if "python" not in words or not words.intersection(SUPPORTED_TERMS):
        return None

    return {
        "id": "remove-negatives",
        "title": "The surviving negative",
        "language": "Python 3",
        "difficulty": "Easy",
        "duration": "10-15 min",
        "topic": "Lists and loops",
        "description": (
            "A filter should remove every negative number from a list, but some "
            "negative values survive. Reproduce the failure and find out why."
        ),
        "workspaceUrl": os.getenv("DEBUG_GYM_WORKSPACE_URL", "http://localhost:8080"),
    }


class CatalogHandler(BaseHTTPRequestHandler):
    """Handle the catalog page and exercise lookup API."""

    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        if self.path in {"/", "/index.html"}:
            self._send_file("index.html", "text/html; charset=utf-8")
        elif self.path == "/styles.css":
            self._send_file("styles.css", "text/css; charset=utf-8")
        elif self.path == "/app.js":
            self._send_file("app.js", "text/javascript; charset=utf-8")
        elif self.path == "/health":
            self._send_json(HTTPStatus.OK, {"status": "ok"})
        else:
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})

    def do_POST(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        if self.path != "/api/exercises":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            query = payload.get("query", "")
            if not isinstance(query, str):
                raise ValueError
        except (json.JSONDecodeError, ValueError):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Send a text query."})
            return

        exercise = find_exercise(query)
        if exercise is None:
            self._send_json(
                HTTPStatus.NOT_FOUND,
                {
                    "error": (
                        "No prepared exercise matches that request. Try a Python "
                        "list, loop, mutation, or negative-number bug."
                    )
                },
            )
            return

        self._send_json(HTTPStatus.OK, {"exercise": exercise})

    def log_message(self, message_format: str, *args: object) -> None:
        print(f"catalog: {message_format % args}")

    def _send_file(self, name: str, content_type: str) -> None:
        data = (STATIC_DIR / name).read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        data = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main() -> None:
    port = int(os.getenv("DEBUG_GYM_CATALOG_PORT", "3000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), CatalogHandler)
    print(f"Debug GYM catalog listening on http://localhost:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
