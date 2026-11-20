import json
from uuid import UUID

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from prometheus_client.parser import text_string_to_metric_families


@override_settings(DEBUG_GYM_METRICS_TOKEN="scraper-test-token")
class ObservabilityTests(TestCase):
    def catalog_count(self, outcome):
        response = self.client.get("/metrics", headers={"Authorization": "Bearer scraper-test-token"})
        self.assertEqual(response.status_code, 200)
        for family in text_string_to_metric_families(response.content.decode()):
            for sample in family.samples:
                if (
                    sample.name == "debug_gym_http_request_duration_seconds_count"
                    and sample.labels == {"route": "/api/exercises", "outcome": outcome}
                ):
                    return sample.value
        self.fail(f"No histogram count for {outcome}")

    def test_catalog_success_and_failure_are_correlated_and_counted(self):
        self.client.force_login(get_user_model().objects.create_user(username="telemetry-test"))
        for query, status, outcome in (
            ("surviving negative", 200, "success"),
            ("javascript promise deadlock", 404, "client_error"),
        ):
            with self.subTest(outcome=outcome):
                count = self.catalog_count(outcome)
                with self.assertLogs("debug_gym.requests", level="INFO") as logs:
                    response = self.client.post(
                        "/api/exercises", {"query": query}, content_type="application/json",
                    )

                self.assertEqual(response.status_code, status)
                self.assertEqual(len(logs.records), 1)
                event = json.loads(logs.records[0].getMessage())
                elapsed = event.pop("duration_ms")
                request_id = response["X-Request-ID"]
                self.assertEqual(UUID(request_id).version, 4)
                self.assertEqual(event, {
                    "event": "catalog_request",
                    "request_id": request_id,
                    "route": "/api/exercises",
                    "outcome": outcome,
                    "status": status,
                })
                self.assertGreaterEqual(elapsed, 0)
                self.assertEqual(self.catalog_count(outcome), count + 1)

    def test_metrics_require_the_configured_token(self):
        self.assertEqual(self.client.get("/metrics").status_code, 404)
        self.assertEqual(
            self.client.get("/metrics", headers={"Authorization": "Bearer wrong"}).status_code, 404,
        )
        with override_settings(DEBUG_GYM_METRICS_TOKEN=""):
            response = self.client.get("/metrics", headers={"Authorization": "Bearer scraper-test-token"})
            self.assertEqual(response.status_code, 404)
