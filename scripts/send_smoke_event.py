"""Send events tagged source=smoke to an analytics backend (FR-014, ADR-006).

Smoke events prove the pipeline end to end without counting as learner
activity: every metric in docs/analytics.md excludes source=smoke. Standard
library only. The key is read from DEBUG_GYM_ANALYTICS_KEY, never from the
command line, so it stays out of shell history.

    python scripts/send_smoke_event.py --url https://analytics.example/events
    python scripts/send_smoke_event.py --url https://analytics.example/events --dry-run
"""

import argparse
import json
import os
import sys
import urllib.request
import uuid
from datetime import datetime, timezone

TIMEOUT_SECONDS = 5


def smoke_events():
    """One smoke event per registry row, from a throwaway random learner."""
    learner = uuid.uuid4().hex
    shared = {"learner_id": learner, "source": "smoke", "exercise_slug": "smoke-test"}
    payloads = [
        {"name": "exercise_searched", "result_count": 1},
        {"name": "exercise_opened"},
        {"name": "workspace_opened"},
        {"name": "solution_verified", "passed_count": 1, "total_count": 1, "all_passed": True},
    ]
    events = []
    for payload in payloads:
        event = {**shared, **payload, "timestamp": datetime.now(timezone.utc).isoformat()}
        if payload["name"] == "exercise_searched":
            del event["exercise_slug"]
        events.append(event)
    return events


def send(url, key, event):
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    request = urllib.request.Request(url, data=json.dumps(event).encode(), headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:  # noqa: S310 - https only
        return response.status


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--url", required=True, help="https:// address of the analytics backend")
    parser.add_argument("--dry-run", action="store_true", help="print the events instead of sending them")
    args = parser.parse_args(argv)
    if not args.url.startswith("https://"):
        print("The backend address must start with https://", file=sys.stderr)
        return 2
    key = os.getenv("DEBUG_GYM_ANALYTICS_KEY", "")
    for event in smoke_events():
        if args.dry_run:
            print(json.dumps(event))
            continue
        try:
            status = send(args.url, key, event)
        except Exception as error:  # noqa: BLE001 - report and fail the script
            print(f"{event['name']}: not delivered ({error})", file=sys.stderr)
            return 1
        print(f"{event['name']}: HTTP {status}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
