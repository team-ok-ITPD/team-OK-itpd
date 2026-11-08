"""Run QR-06 QRT-01: fail one staging request and find it in the observability backend.

The script signs in to the staging deployment, sends one search that succeeds
and one that fails with a 404, then queries the staging organization of the
observability backend for the failed request's log point and for the P95 of
SLI-01 (docs/observability.md#sli-01). It uses only the standard library.

Configuration comes from the environment and is never committed:

    STAGING_URL           address of the staging catalog
    OPENOBSERVE_URL       address of the observability backend
    OPENOBSERVE_ORG       the staging organization
    OPENOBSERVE_USER      backend user, with OPENOBSERVE_PASSWORD
    OPENOBSERVE_PASSWORD
    STAGING_LOGIN         a staging learner's username or email,
    STAGING_PASSWORD      with that learner's password

Exit status is 0 when both checks pass and 1 otherwise.
"""

import base64
import http.cookiejar
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

LOG_DEADLINE_SECONDS = 5
SLI_DEADLINE_SECONDS = 60
LOG_STREAM = "debug_gym_requests"
SLI_QUERY = (
    "histogram_quantile(0.95, sum by (le, route, outcome) "
    '(rate(debug_gym_http_request_duration_seconds_bucket{route="/api/exercises"}[5m])))'
)


def required(name):
    value = os.getenv(name, "")
    if not value:
        sys.exit(f"Set {name} in the environment.")
    return value


class Staging:
    def __init__(self, base):
        self.base = base.rstrip("/")
        self.jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))

    def csrf(self):
        return next((c.value for c in self.jar if c.name == "csrftoken"), "")

    def post(self, path, payload):
        request = urllib.request.Request(
            self.base + path,
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json", "X-CSRFToken": self.csrf(), "Referer": self.base + "/"},
            method="POST",
        )
        try:
            with self.opener.open(request, timeout=10) as response:
                return response.status, response.headers.get("X-Request-ID", "")
        except urllib.error.HTTPError as error:
            return error.code, error.headers.get("X-Request-ID", "")

    def sign_in(self, login, password):
        self.opener.open(self.base + "/", timeout=10).read()  # sets the CSRF cookie
        status, _ = self.post("/api/auth/login/", {"login": login, "password": password})
        if status != 200:
            sys.exit(f"Sign-in to staging failed with HTTP {status}.")


def backend_get(url, user, password):
    token = base64.b64encode(f"{user}:{password}".encode()).decode()
    request = urllib.request.Request(url, headers={"Authorization": f"Basic {token}"})
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.load(response)


def backend_search(base, org, user, password, sql):
    now = int(time.time() * 1_000_000)
    body = {"query": {"sql": sql, "start_time": now - 10 * 60 * 1_000_000, "end_time": now, "from": 0, "size": 10}}
    request = urllib.request.Request(
        f"{base}/api/{org}/_search?type=logs",
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Basic " + base64.b64encode(f"{user}:{password}".encode()).decode(),
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.load(response).get("hits", [])


def wait_for(deadline_seconds, attempt):
    """Call attempt() about once a second until it returns something or time runs out."""
    end = time.monotonic() + deadline_seconds
    while True:
        found = attempt()
        if found:
            return found
        if time.monotonic() >= end:
            return None
        time.sleep(1)


def main():
    staging = Staging(required("STAGING_URL"))
    backend = required("OPENOBSERVE_URL").rstrip("/")
    org, user, password = required("OPENOBSERVE_ORG"), required("OPENOBSERVE_USER"), required("OPENOBSERVE_PASSWORD")

    staging.sign_in(required("STAGING_LOGIN"), required("STAGING_PASSWORD"))
    ok_status, _ = staging.post("/api/exercises", {"query": "remove negatives"})
    failed_status, request_id = staging.post("/api/exercises", {"query": "zzzqqq no such exercise"})
    print(f"baseline search: HTTP {ok_status}; failed search: HTTP {failed_status}; request_id: {request_id}")
    if failed_status != 404 or not request_id:
        print("The failed request did not return 404 with an X-Request-ID.", file=sys.stderr)
        return 1

    sql = (
        "SELECT request_id, route, outcome, status, duration_ms "
        f'FROM "{LOG_STREAM}" WHERE request_id = \'{request_id}\''
    )
    hits = wait_for(LOG_DEADLINE_SECONDS, lambda: backend_search(backend, org, user, password, sql))
    if not hits or len(hits) != 1:
        print(f"FAIL: no single log point for {request_id} within {LOG_DEADLINE_SECONDS} seconds.", file=sys.stderr)
        return 1
    print("log point:", json.dumps(hits[0], sort_keys=True))

    def p95():
        query = urllib.parse.urlencode({"query": SLI_QUERY})
        data = backend_get(f"{backend}/api/{org}/prometheus/api/v1/query?{query}", user, password)
        for series in data.get("data", {}).get("result", []):
            if series.get("metric", {}).get("outcome") == "client_error":
                value = float(series["value"][1])
                if value == value:  # not NaN
                    return series
        return None

    series = wait_for(SLI_DEADLINE_SECONDS, p95)
    if series is None:
        print(f"FAIL: no numeric client_error P95 within {SLI_DEADLINE_SECONDS} seconds.", file=sys.stderr)
        return 1
    print("SLI-01 client_error P95 (seconds):", series["value"][1])
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
