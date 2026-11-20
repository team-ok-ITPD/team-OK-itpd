import json
import logging
from secrets import compare_digest
from time import perf_counter
from uuid import uuid4

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_safe
from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, Histogram, generate_latest


CATALOG_ROUTE = "/api/exercises"
logger = logging.getLogger("debug_gym.requests")
registry = CollectorRegistry()
duration = Histogram(
    "debug_gym_http_request_duration_seconds",
    "Time spent handling an instrumented Django HTTP request.",
    ("route", "outcome"),
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10),
    registry=registry,
)

# A scrape before the first error must include its zero-valued buckets.
for outcome in ("success", "client_error", "server_error"):
    duration.labels(route=CATALOG_ROUTE, outcome=outcome)


def catalog_request_telemetry(get_response):
    def middleware(request):
        if request.method != "POST" or request.path_info != CATALOG_ROUTE:
            return get_response(request)

        request_id = uuid4().hex
        start = perf_counter()
        response = get_response(request)
        elapsed = perf_counter() - start
        status = response.status_code
        if status >= 500:
            outcome = "server_error"
        elif status >= 400:
            outcome = "client_error"
        else:
            outcome = "success"

        duration.labels(route=CATALOG_ROUTE, outcome=outcome).observe(elapsed)
        logger.info(json.dumps({
            "event": "catalog_request",
            "request_id": request_id,
            "route": CATALOG_ROUTE,
            "outcome": outcome,
            "status": status,
            "duration_ms": round(elapsed * 1000, 3),
        }))
        response["X-Request-ID"] = request_id
        return response

    return middleware


@never_cache
@require_safe
def metrics(request):
    token = settings.DEBUG_GYM_METRICS_TOKEN
    authorization = request.headers.get("Authorization", "")
    if not token or not compare_digest(authorization.encode(), f"Bearer {token}".encode()):
        return HttpResponseNotFound()
    return HttpResponse(generate_latest(registry), content_type=CONTENT_TYPE_LATEST)
