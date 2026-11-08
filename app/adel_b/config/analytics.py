"""Record analytics events and send them to the external analytics backend.

Events follow the registry in docs/analytics.md#the-events. Collection is off
unless DEBUG_GYM_ANALYTICS_URL is an https address, and no failure here ever
reaches the request that produced the event (FR-014, ADR-006).
"""

import json
import logging
import queue
import threading
import urllib.request
from datetime import datetime, timezone

from django.conf import settings

logger = logging.getLogger("debug_gym.analytics")

SOURCES = ("web", "usability-test", "smoke")

# One entry per row of the event table; every listed field is required.
EVENTS = {
    "exercise_searched": {"result_count": int},
    "exercise_opened": {"exercise_slug": str},
    "workspace_opened": {"exercise_slug": str},
    "solution_verified": {
        "exercise_slug": str,
        "passed_count": int,
        "total_count": int,
        "all_passed": bool,
    },
}

QUEUE_SIZE = 200
SEND_TIMEOUT_SECONDS = 2

_queue = queue.Queue(maxsize=QUEUE_SIZE)
_worker = None
_worker_lock = threading.Lock()


def learner_id(user):
    """The learner's opaque analytics identifier.

    It is a random UUID stored on the profile: it is not derived from the
    username, the email or any other personal data, and it cannot be reversed
    to them.
    """
    from accounts.models import Profile

    profile, _ = Profile.objects.get_or_create(user=user)
    return profile.analytics_id.hex


def build_event(name, user, source="web", **fields):
    """Return the event payload, or raise ValueError when it breaks the registry."""
    schema = EVENTS.get(name)
    if schema is None:
        raise ValueError(f"Unknown analytics event {name!r}.")
    if source not in SOURCES:
        raise ValueError(f"Unknown analytics source {source!r}.")
    if not user.is_authenticated:
        raise ValueError("An analytics event needs a signed-in learner.")
    if set(fields) != set(schema):
        raise ValueError(f"{name} takes exactly the fields {sorted(schema)}.")
    for field, expected in schema.items():
        if type(fields[field]) is not expected:
            raise ValueError(f"{name}.{field} must be {expected.__name__}.")
    return {
        "name": name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "learner_id": learner_id(user),
        "source": source,
        **fields,
    }


def _target():
    url = getattr(settings, "DEBUG_GYM_ANALYTICS_URL", "")
    if not url:
        return None
    if not url.startswith("https://"):
        logger.warning("Analytics collection is off: the backend address must use https.")
        return None
    return url, getattr(settings, "DEBUG_GYM_ANALYTICS_KEY", "")


def _post(url, key, event):
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    request = urllib.request.Request(
        url, data=json.dumps(event).encode(), headers=headers, method="POST"
    )
    with urllib.request.urlopen(request, timeout=SEND_TIMEOUT_SECONDS):  # noqa: S310 - https only
        pass


def _run():
    while True:
        url, key, event = _queue.get()
        try:
            _post(url, key, event)
        except Exception:  # noqa: BLE001 - delivery must never raise into the product
            logger.warning("Analytics event %s was not delivered.", event.get("name"))
        finally:
            _queue.task_done()


def _ensure_worker():
    global _worker
    with _worker_lock:
        if _worker is None or not _worker.is_alive():
            _worker = threading.Thread(target=_run, name="analytics", daemon=True)
            _worker.start()


def emit(name, user, *, source="web", **fields):
    """Queue one event for delivery; return whether it was queued.

    Returns False without raising when collection is off, the event breaks the
    registry or the queue is full, so a caller can emit from any request.
    """
    try:
        target = _target()
        if target is None:
            return False
        event = build_event(name, user, source, **fields)
        _queue.put_nowait((*target, event))
        _ensure_worker()
        return True
    except queue.Full:
        logger.warning("Analytics queue is full; dropped %s.", name)
    except Exception as error:  # noqa: BLE001 - never break the request
        logger.warning("Analytics event %s was not recorded: %s", name, error)
    return False


def flush():
    """Wait until every queued event has been attempted (for tests and shutdown)."""
    _queue.join()
