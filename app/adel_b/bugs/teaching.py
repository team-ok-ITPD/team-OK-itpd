"""Professor and student APIs for exercises and assignments."""

import datetime
import json
import keyword
import re

from django.http import JsonResponse
from django.utils.text import slugify
from django.views.decorators.http import require_http_methods

from accounts.permissions import professor_required_json

from .models import Assignment, Attempt, Bug, Draft, TeachingGroup
from .views import MAX_DRAFT_LENGTH, LiteralError, login_required_json, parse_test_value

TOPICS = {"arrays": "Arrays & loops", "dicts": "Dictionaries", "strings": "Strings", "other": "Other"}
DIFFICULTIES = ("Easy", "Medium", "Hard")
MAX_TESTS = 20


def _read_json(request):
    try:
        payload = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def _text(payload, name, limit, required=False, errors=None):
    value = payload.get(name, "")
    if not isinstance(value, str):
        errors[name] = "Enter text."
        return ""
    value = value.strip()
    if required and not value:
        errors[name] = "This field is required."
    elif len(value) > limit:
        errors[name] = f"Keep it under {limit} characters."
    return value


def clean_exercise(payload):
    """Validate an exercise sent by the editor; return (model fields, errors by field)."""
    errors = {}
    fields = {
        "title": _text(payload, "title", 200, required=True, errors=errors),
        "summary": _text(payload, "summary", 200, errors=errors),
        "description": _text(payload, "description", 5000, required=True, errors=errors),
        "symptom": _text(payload, "symptom", 200, errors=errors),
        "explanation": _text(payload, "explanation", 5000, errors=errors),
    }

    difficulty = payload.get("difficulty", "Easy")
    if difficulty not in DIFFICULTIES:
        errors["difficulty"] = f"Choose one of {', '.join(DIFFICULTIES)}."
    category = payload.get("topic", "other")
    if category not in TOPICS:
        errors["topic"] = f"Choose one of {', '.join(TOPICS)}."
    fields.update(difficulty=difficulty, category=category, topic=TOPICS.get(category, ""))

    function = _text(payload, "functionName", 100, required=True, errors=errors)
    if function and (not function.isidentifier() or keyword.iskeyword(function)):
        errors["functionName"] = "Use a Python function name, like remove_negatives."
    # Without a file name, use the function's; an invalid function name is reported on its own.
    default_file = f"{function}.py" if function and "functionName" not in errors else ""
    file_name = _text(payload, "file", 100, errors=errors) or default_file
    stem = file_name[:-3] if file_name.endswith(".py") else ""
    if "file" not in errors and file_name and (not stem.isidentifier() or keyword.iskeyword(stem)):
        errors["file"] = "Use a Python file name, like remove_negatives.py."
    fields.update(function_name=function, file_name=file_name)

    code = payload.get("buggyCode", "")
    if not isinstance(code, str) or not code.strip():
        errors["buggyCode"] = "Paste the buggy code."
    elif len(code) > MAX_DRAFT_LENGTH:
        errors["buggyCode"] = "The code is too long."
    elif function and "functionName" not in errors and not re.search(rf"^\s*def\s+{function}\s*\(", code, re.M):
        errors["buggyCode"] = f"The code must define {function}()."
    fields["buggy_code"] = code if isinstance(code, str) else ""

    fields["tests"] = _clean_tests(payload.get("tests"), errors)
    return fields, errors


def _clean_tests(tests, errors):
    if not isinstance(tests, list) or not tests:
        errors["tests"] = "Add at least one test."
        return []
    if len(tests) > MAX_TESTS:
        errors["tests"] = f"Use at most {MAX_TESTS} tests."
        return []
    cleaned = []
    for index, test in enumerate(tests):
        prefix = f"tests.{index}"
        if not isinstance(test, dict):
            errors[prefix] = "Each test needs a name, an input and an expected value."
            continue
        name = test.get("name", "")
        if not isinstance(name, str) or not name.strip():
            errors[f"{prefix}.name"] = "Give the test a name."
        values = {}
        for field in ("input", "expected"):
            try:
                values[field] = parse_test_value(test.get(field))
            except LiteralError as error:
                errors[f"{prefix}.{field}"] = str(error)
        if len(values) == 2 and isinstance(name, str) and name.strip():
            cleaned.append({"name": name.strip()[:100], **values})
    return cleaned


def _unique_slug(title):
    base = slugify(title)[:40].strip("-") or "exercise"
    slug, number = base, 2
    while Bug.objects.filter(slug=slug).exists():
        slug, number = f"{base}-{number}", number + 1
    return slug


def student_status(student, bug):
    """How far a student is on a bug: not-started, progress, failed or solved."""
    attempts = list(Attempt.objects.filter(user=student, bug=bug))
    draft = Draft.objects.filter(user=student, bug=bug).first()
    best = max(attempts, key=lambda attempt: (attempt.passed_count, attempt.created_at), default=None)
    if any(attempt.solved for attempt in attempts):
        status = "solved"
    elif attempts:
        status = "failed"
    elif draft is not None:
        status = "progress"
    else:
        status = "not-started"
    times = [attempt.created_at for attempt in attempts] + ([draft.updated_at] if draft else [])
    return {
        "status": status,
        "attempts": len(attempts),
        "bestPassed": best.passed_count if best else None,
        "total": len(bug.tests),
        "lastActivity": max(times).isoformat() if times else None,
    }


def _own_bug(request, slug):
    return Bug.objects.filter(slug=slug, created_by=request.user).first()


def _editor_dict(bug):
    """The exercise as the editor shows it, with test values written as Python."""
    return {
        **bug.to_dict(),
        "editTests": [
            {"name": test["name"], "input": repr(test["input"]), "expected": repr(test["expected"])}
            for test in bug.tests
        ],
    }


@require_http_methods(["GET", "POST"])
@professor_required_json
def exercises(request):
    if request.method == "GET":
        items = []
        for bug in Bug.objects.filter(created_by=request.user).order_by("-created_at"):
            students = {
                membership.student
                for assignment in bug.assignments.prefetch_related("group__memberships__student")
                for membership in assignment.group.memberships.all()
            }
            solved = sum(1 for student in students if student_status(student, bug)["status"] == "solved")
            items.append({
                **bug.to_dict(),
                "assigned": bug.assignments.count(),
                "assignedStudents": len(students),
                "solved": solved,
            })
        return JsonResponse({"exercises": items})

    payload = _read_json(request)
    if payload is None:
        return JsonResponse({"error": "Send a JSON object."}, status=400)
    fields, errors = clean_exercise(payload)
    if errors:
        return JsonResponse({"error": "Please fix the highlighted fields.", "fields": errors}, status=400)
    bug = Bug.objects.create(slug=_unique_slug(fields["title"]), created_by=request.user, **fields)
    return JsonResponse({"exercise": _editor_dict(bug)}, status=201)


@require_http_methods(["GET", "PUT", "DELETE"])
@professor_required_json
def exercise(request, slug):
    bug = _own_bug(request, slug)
    if bug is None:
        return JsonResponse({"error": "Exercise not found."}, status=404)
    if request.method == "GET":
        return JsonResponse({"exercise": _editor_dict(bug)})
    if request.method == "DELETE":
        bug.delete()
        return JsonResponse({"deleted": slug})

    payload = _read_json(request)
    if payload is None:
        return JsonResponse({"error": "Send a JSON object."}, status=400)
    fields, errors = clean_exercise(payload)
    if errors:
        return JsonResponse({"error": "Please fix the highlighted fields.", "fields": errors}, status=400)
    if fields["tests"] != bug.tests:
        # Learners' edited copies of the old tests no longer line up with the new ones.
        Draft.objects.filter(bug=bug).update(tests=None)
    for name, value in fields.items():
        setattr(bug, name, value)
    bug.save()
    return JsonResponse({"exercise": _editor_dict(bug)})


@require_http_methods(["PUT"])
@professor_required_json
def audience(request, slug):
    bug = _own_bug(request, slug)
    if bug is None:
        return JsonResponse({"error": "Exercise not found."}, status=404)
    payload = _read_json(request)
    value = payload.get("audience") if payload else None
    if value not in {Bug.PRIVATE, Bug.PUBLIC, Bug.GROUP}:
        return JsonResponse({"error": "Choose private, public or group access."}, status=400)
    if value == Bug.GROUP and not bug.assignments.exists():
        return JsonResponse({"error": "Assign this exercise to a group first."}, status=400)
    bug.audience = value
    bug.save(update_fields=["audience"])
    return JsonResponse({"exercise": _editor_dict(bug)})


@require_http_methods(["GET"])
@professor_required_json
def groups(request):
    owned = TeachingGroup.objects.filter(teacher=request.user).order_by("name")
    return JsonResponse({
        "groups": [
            {"id": group.id, "name": group.name, "memberCount": group.memberships.count()}
            for group in owned
        ]
    })


def _assignment_rows(bug):
    rows = []
    assignments = bug.assignments.select_related("group").prefetch_related("group__memberships__student")
    for assignment in assignments:
        members = []
        for membership in assignment.group.memberships.all():
            student = membership.student
            members.append({
                "studentId": student.id,
                "username": student.username,
                "email": student.email,
                **student_status(student, bug),
            })
        rows.append({
            "assignmentId": assignment.id,
            "groupId": assignment.group_id,
            "groupName": assignment.group.name,
            "deadline": assignment.deadline.isoformat() if assignment.deadline else None,
            "members": sorted(members, key=lambda row: row["username"].lower()),
        })
    return sorted(rows, key=lambda row: row["groupName"].lower())


@require_http_methods(["GET", "POST"])
@professor_required_json
def assignments(request, slug):
    bug = _own_bug(request, slug)
    if bug is None:
        return JsonResponse({"error": "Exercise not found."}, status=404)
    if request.method == "GET":
        return JsonResponse({"assignments": _assignment_rows(bug)})

    payload = _read_json(request)
    ids = payload.get("groups") if payload else None
    if not isinstance(ids, list) or not ids or not all(type(value) is int for value in ids):
        return JsonResponse({"error": "Choose at least one group."}, status=400)
    value = payload.get("deadline")
    deadline = None
    if value not in (None, ""):
        try:
            deadline = datetime.date.fromisoformat(value)
        except (TypeError, ValueError):
            return JsonResponse({"error": "Use a deadline like 2026-12-01."}, status=400)
    chosen = list(TeachingGroup.objects.filter(teacher=request.user, id__in=ids))
    if len(chosen) != len(set(ids)):
        return JsonResponse({"error": "Only your groups can be assigned an exercise."}, status=400)
    for group in chosen:
        Assignment.objects.update_or_create(bug=bug, group=group, defaults={"deadline": deadline})
    return JsonResponse({"assignments": _assignment_rows(bug)})


@require_http_methods(["DELETE"])
@professor_required_json
def unassign(request, slug, assignment_id):
    bug = _own_bug(request, slug)
    if bug is None:
        return JsonResponse({"error": "Exercise not found."}, status=404)
    Assignment.objects.filter(id=assignment_id, bug=bug, group__teacher=request.user).delete()
    if bug.audience == Bug.GROUP and not bug.assignments.exists():
        bug.audience = Bug.PRIVATE
        bug.save(update_fields=["audience"])
    return JsonResponse({"assignments": _assignment_rows(bug), "audience": bug.audience})


@require_http_methods(["GET"])
@login_required_json
def my_assignments(request):
    """The logged-in student's group assignments, earliest deadline first."""
    today = datetime.date.today()
    items = []
    assignments = Assignment.objects.filter(
        group__memberships__student=request.user, bug__audience=Bug.GROUP
    ).select_related("bug", "group__teacher")
    for assignment in assignments:
        bug = assignment.bug
        progress = student_status(request.user, bug)
        items.append({
            "bugId": bug.slug,
            "title": bug.title,
            "summary": bug.summary,
            "difficulty": bug.difficulty,
            "assignmentId": assignment.id,
            "groupId": assignment.group_id,
            "groupName": assignment.group.name,
            "assignedBy": assignment.group.teacher.username,
            "deadline": assignment.deadline.isoformat() if assignment.deadline else None,
            "overdue": bool(assignment.deadline and assignment.deadline < today and progress["status"] != "solved"),
            **progress,
        })
    return JsonResponse({"assignments": items})
