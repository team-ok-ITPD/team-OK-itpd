import ast
import json
import math
import re
from functools import wraps
from pathlib import Path

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from .models import Attempt, Bug, Draft, IdeToken

REQUIRED_FIELDS = ("slug", "title", "description")
EDITABLE_FIELDS = {
    "slug": "slug",
    "title": "title",
    "language": "language",
    "difficulty": "difficulty",
    "duration": "duration",
    "topic": "category",
    "topicLabel": "topic",
    "summary": "summary",
    "description": "description",
    "file": "file_name",
    "functionName": "function_name",
    "buggyCode": "buggy_code",
    "tests": "tests",
    "symptom": "symptom",
    "explanation": "explanation",
    "workspace": "has_workspace",
}
MAX_DRAFT_LENGTH = 50_000
MAX_VALUE_LENGTH = 2_000
STOP_WORDS = {"a", "an", "and", "bug", "for", "in", "of", "the", "to", "with", "python"}


def login_required_json(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Log in to continue."}, status=401)
        return view(request, *args, **kwargs)

    return wrapper


@require_http_methods(["GET", "POST"])
def bug_list(request):
    if request.method == "GET":
        return JsonResponse({"bugs": [bug.to_dict() for bug in Bug.objects.all()]})

    if not request.user.is_staff:
        return JsonResponse({"error": "Only staff can add bugs."}, status=403)
    try:
        payload = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Send a JSON body."}, status=400)
    if not isinstance(payload, dict):
        return JsonResponse({"error": "Send a JSON object."}, status=400)

    missing = [name for name in REQUIRED_FIELDS if not payload.get(name)]
    if missing:
        return JsonResponse({"error": f"Missing fields: {', '.join(missing)}."}, status=400)
    if Bug.objects.filter(slug=payload["slug"]).exists():
        return JsonResponse({"error": "A bug with that id already exists."}, status=409)

    fields = {model: payload[key] for key, model in EDITABLE_FIELDS.items() if key in payload}
    bug = Bug.objects.create(**fields)
    return JsonResponse({"bug": bug.to_dict()}, status=201)


@require_http_methods(["GET"])
def bug_detail(request, slug):
    bug = Bug.objects.filter(slug=slug).first()
    if bug is None:
        return JsonResponse({"error": "Bug not found."}, status=404)
    return JsonResponse({"bug": bug.to_dict()})


@require_http_methods(["GET"])
def health(request):
    return JsonResponse({"status": "ok"})


@require_http_methods(["GET", "PUT", "DELETE"])
@login_required_json
def bug_draft(request, slug):
    bug = Bug.objects.filter(slug=slug).first()
    if bug is None:
        return JsonResponse({"error": "Bug not found."}, status=404)

    if request.method == "GET":
        draft = Draft.objects.filter(user=request.user, bug=bug).first()
        if draft is None:
            return JsonResponse({"draft": None})
        return JsonResponse({"draft": draft.to_dict()})

    if request.method == "DELETE":
        draft = Draft.objects.filter(user=request.user, bug=bug).first()
        if draft is None or draft.tests is None:
            Draft.objects.filter(user=request.user, bug=bug).delete()
            return JsonResponse({"draft": None})
        # Keep the learner's edited tests; only the code goes back to the original.
        draft.code = bug.buggy_code
        draft.save()
        return JsonResponse({"draft": draft.to_dict()})

    try:
        payload = json.loads(request.body or b"{}")
        code = payload.get("code")
        if not isinstance(code, str):
            raise ValueError
    except (json.JSONDecodeError, AttributeError, ValueError):
        return JsonResponse({"error": "Send the code as text."}, status=400)
    if len(code) > MAX_DRAFT_LENGTH:
        return JsonResponse({"error": "The code is too long to save."}, status=400)

    draft, _ = Draft.objects.update_or_create(user=request.user, bug=bug, defaults={"code": code})
    return JsonResponse({"draft": draft.to_dict()})


@require_http_methods(["GET", "POST"])
@login_required_json
def bug_attempts(request, slug):
    bug = Bug.objects.filter(slug=slug).first()
    if bug is None:
        return JsonResponse({"error": "Bug not found."}, status=404)

    if request.method == "GET":
        attempts = bug.attempts.filter(user=request.user)
        return JsonResponse({"attempts": [attempt.to_dict() for attempt in attempts]})

    try:
        payload = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        payload = None
    return _save_attempt(request.user, bug, payload)


def _save_attempt(user, bug, payload):
    try:
        code, passed, total = payload.get("code"), payload.get("passed"), payload.get("total")
        if not isinstance(code, str) or type(passed) is not int or type(total) is not int:
            raise ValueError
    except (AttributeError, ValueError):
        return JsonResponse({"error": "Send the code and the passed and total test counts."}, status=400)
    if len(code) > MAX_DRAFT_LENGTH:
        return JsonResponse({"error": "The code is too long to save."}, status=400)
    if total != len(bug.tests) or not 0 <= passed <= total:
        return JsonResponse({"error": f"This bug has {len(bug.tests)} tests."}, status=400)

    attempt = Attempt.objects.create(user=user, bug=bug, code=code, passed_count=passed, total_count=total)
    return JsonResponse({"attempt": attempt.to_dict()}, status=201)


# The extension authenticates with its token, not a session cookie, so CSRF does not apply.
@csrf_exempt
@require_http_methods(["POST"])
def ide_submit(request):
    """Save an attempt sent by the Debug GYM VS Code extension."""
    scheme, _, key = request.headers.get("Authorization", "").partition(" ")
    token = IdeToken.find(key.strip()) if scheme.lower() == "bearer" and key.strip() else None
    if token is None:
        return JsonResponse(
            {"error": "This VS Code folder is no longer connected. Open it again from the website."},
            status=401,
        )
    try:
        payload = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        payload = None
    if isinstance(payload, dict) and payload.get("bug") != token.bug.slug:
        return JsonResponse({"error": "This folder belongs to another exercise."}, status=400)
    response = _save_attempt(token.user, token.bug, payload)
    if response.status_code == 201:
        # The website and the next VS Code opening show the code the learner submitted.
        Draft.objects.update_or_create(
            user=token.user, bug=token.bug, defaults={"code": payload["code"]}
        )
    return response


@require_http_methods(["GET"])
@login_required_json
def history(request):
    """Return each bug the learner has touched, newest first, with its status."""
    attempts_by_bug, drafts_by_bug = {}, {}
    for attempt in request.user.attempts.all():
        attempts_by_bug.setdefault(attempt.bug_id, []).append(attempt)
    for draft in request.user.drafts.all():
        drafts_by_bug[draft.bug_id] = draft

    items = []
    for bug in Bug.objects.filter(id__in=attempts_by_bug.keys() | drafts_by_bug.keys()):
        attempts = attempts_by_bug.get(bug.id, [])
        draft = drafts_by_bug.get(bug.id)
        if any(attempt.solved for attempt in attempts):
            status = "solved"
        elif attempts:
            status = "failed"
        else:
            status = "progress"
        times = [attempt.created_at for attempt in attempts[:1]]
        if draft is not None:
            times.append(draft.updated_at)
        items.append({
            "bugId": bug.slug,
            "title": bug.title,
            "status": status,
            "lastActivity": max(times).isoformat(),
        })
    items.sort(key=lambda item: item["lastActivity"], reverse=True)
    activity = [
        moment.isoformat()
        for moment in request.user.attempts.values_list("created_at", flat=True)[:500]
    ]
    return JsonResponse({"items": items, "activity": activity})


class LiteralError(ValueError):
    pass


def parse_test_value(text):
    """Read a Python literal such as [1, -2] or {'a': 1} into a JSON-safe value."""
    if not isinstance(text, str) or not text.strip():
        raise LiteralError("Enter a Python value, for example [1, -2, 3].")
    if len(text) > MAX_VALUE_LENGTH:
        raise LiteralError(f"Keep the value under {MAX_VALUE_LENGTH} characters.")
    try:
        value = ast.literal_eval(text.strip())
    except (ValueError, SyntaxError, TypeError, MemoryError, RecursionError):
        raise LiteralError("That is not a Python value. Try something like [1, -2, 3] or 'text'.")
    return _json_safe(value)


def _json_safe(value):
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise LiteralError("Use a finite number.")
        return value
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise LiteralError("Dictionary keys must be strings in tests.")
        return {key: _json_safe(item) for key, item in value.items()}
    raise LiteralError(
        f"Tests can use lists, dicts, strings, numbers, True/False and None, not {type(value).__name__}."
    )


@require_http_methods(["PUT", "DELETE"])
@login_required_json
def bug_test(request, slug, index):
    """Edit (PUT) or restore (DELETE) one of the learner's copies of a bug's tests."""
    bug = Bug.objects.filter(slug=slug).first()
    if bug is None:
        return JsonResponse({"error": "Bug not found."}, status=404)
    if not 0 <= index < len(bug.tests):
        return JsonResponse({"error": "Test not found."}, status=404)

    draft = Draft.objects.filter(user=request.user, bug=bug).first()
    tests = [dict(test) for test in (draft.tests if draft and draft.tests else bug.tests)]

    if request.method == "DELETE":
        tests[index] = dict(bug.tests[index])
    else:
        try:
            payload = json.loads(request.body or b"{}")
            if not isinstance(payload, dict):
                raise ValueError
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({"error": "Send a JSON object."}, status=400)
        errors = {}
        values = {}
        for field in ("input", "expected"):
            try:
                values[field] = parse_test_value(payload.get(field))
            except LiteralError as error:
                errors[field] = str(error)
        if errors:
            return JsonResponse({"error": "Please fix the test values.", "fields": errors}, status=400)
        tests[index] = {**tests[index], **values}

    edited = None if tests == bug.tests else tests
    if draft is None:
        if edited is None:
            return JsonResponse({"tests": bug.tests, "edited": False})
        draft = Draft(user=request.user, bug=bug, code=bug.buggy_code)
    draft.tests = edited
    draft.save()
    return JsonResponse({"tests": draft.tests or bug.tests, "edited": draft.tests is not None})


@require_http_methods(["POST"])
@login_required_json
def bug_vscode(request, slug):
    """Write the learner's workspace for this bug and open it in their VS Code container."""
    # Imported here: both modules import from this one.
    from .ide import IdeError, start_ide
    from .workspaces import WorkspaceError, write_workspace

    bug = Bug.objects.filter(slug=slug).first()
    if bug is None:
        return JsonResponse({"error": "Bug not found."}, status=404)
    try:
        folder = write_workspace(request.user, bug)
    except WorkspaceError as error:
        return JsonResponse({"error": str(error)}, status=400)
    try:
        port = start_ide(request.user, folder)
    except IdeError as error:
        return JsonResponse({"error": str(error)}, status=503)
    return JsonResponse({"url": f"http://localhost:{port}/?folder=/home/coder/project"})


def _words(text):
    return {word for word in re.findall(r"[a-z]+", text.lower()) if word not in STOP_WORDS}


def _stem(word):
    return word[:-1] if word.endswith("s") else word


MIN_PREFIX = 3


def _title_hits(wanted, title):
    """Count query words that start a title word (or the reverse), so "dup" finds "Duplicate"."""
    title_words = {_stem(word) for word in _words(title)}
    return sum(
        1
        for word in wanted
        if len(word) >= MIN_PREFIX
        and any(
            title_word.startswith(word) or (len(title_word) >= MIN_PREFIX and word.startswith(title_word))
            for title_word in title_words
        )
    )


def rank_bugs(query):
    """Return (bugs, "title" | "description"): title matches first, else description matches.

    Bugs whose title matches are ranked by matched words, an exact phrase from the title
    ranking highest. Only when no title matches do summaries and descriptions count.
    """
    wanted = {_stem(word) for word in _words(query)}
    phrase = " ".join(query.lower().split())
    bugs = list(Bug.objects.all())

    def order(item):
        score, bug = item
        # Ties keep catalog order, with bugs that have a prepared workspace first.
        return (-score, not bug.has_workspace, bug.id)

    by_title = []
    for bug in bugs:
        score = _title_hits(wanted, bug.title) * 10
        if len(phrase) >= MIN_PREFIX and phrase in bug.title.lower():
            score += 100
        if score:
            by_title.append((score, bug))
    if by_title:
        return [bug for _, bug in sorted(by_title, key=order)], "title"

    by_text = []
    for bug in bugs:
        text = " ".join([bug.summary, bug.description, bug.topic, bug.category])
        score = len(wanted & {_stem(word) for word in _words(text)})
        if score:
            by_text.append((score, bug))
    return [bug for _, bug in sorted(by_text, key=order)], "description"


def match_bug(query):
    """Return the stored bug whose text shares the most words with the query."""
    ranked, _ = rank_bugs(query)
    return ranked[0] if ranked else None


@require_http_methods(["POST"])
def exercise_match(request):
    try:
        payload = json.loads(request.body or b"{}")
        query = payload.get("query", "")
        if not isinstance(query, str):
            raise ValueError
    except (json.JSONDecodeError, AttributeError, ValueError):
        return JsonResponse({"error": "Send a text query."}, status=400)

    ranked, matched_by = rank_bugs(query)
    if not ranked:
        return JsonResponse(
            {"error": "No prepared exercise matches that request. Try a Python list, loop, or dictionary bug."},
            status=404,
        )
    # "exercise" is the best match; "exercises" lists every related one, best first.
    return JsonResponse({
        "exercise": ranked[0].to_dict(),
        "exercises": [bug.to_dict() for bug in ranked],
        "matchedBy": matched_by,
    })


def _asset_version():
    """Changes whenever a page asset changes, so browsers never run an old app.js."""
    folder = Path(__file__).resolve().parent / "static" / "bugs"
    return str(max(int(path.stat().st_mtime) for path in folder.iterdir() if path.is_file()))


@ensure_csrf_cookie
def index(request):
    return render(request, "bugs/index.html", {"asset_version": _asset_version()})
