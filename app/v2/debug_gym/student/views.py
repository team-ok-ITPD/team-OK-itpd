# [Student Dev] Views for student pages: assignments, bug workspace, practice, results
import json
from datetime import timedelta

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Max, Q
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.utils import timezone
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_POST

from core.models import Assignment, Bug, StudyGroup, Submission
from core.permissions import student_required

from app.adel_b.bugs.verification import VerificationBusy
from core.runtime import RuntimeError as VerificationError
from core.bridge import ensure_relay, ide_server_url
from core.runtime import verify

from . import ai
from .forms import AIBugForm, StudentBugForm, SubmissionForm
from .ide import IdeError, start_ide
from .models import IdeToken
from .workspaces import build_project, code_file_name, has_tests, project_has_tests, write_workspace

DUE_SOON = timedelta(hours=48)
DASHBOARD_LIMIT = 5
HISTORY_PAGE_SIZE = 20

# Status of an assignment for one student, with its label and badge class.
STATUSES = {
    "todo": ("To do", ""),
    "submitted": ("Submitted", "warning"),
    "graded": ("Graded", "success"),
    "missed": ("Missed", "danger"),
}


def my_assignments(student):
    """Every assignment sent to one of the student's groups."""
    return (
        Assignment.objects.filter(groups__students=student)
        .select_related("bug", "professor")
        .distinct()
    )


def is_open(assignment, now=None):
    """Whether the assignment still accepts submissions."""
    now = now or timezone.now()
    return assignment.status == Assignment.Status.ACTIVE and (
        assignment.deadline is None or assignment.deadline >= now
    )


def best_submission(submissions):
    """The submission that counts (DEC-022): the most tests passed, then the newest.

    Submissions without recorded test counts rank below any with counts, so when
    none has counts the newest one counts. Returns None for an empty list.
    """
    return max(
        submissions,
        key=lambda s: (
            s.tests_passed if s.tests_passed is not None else -1,
            s.submitted_at,
            s.pk,
        ),
        default=None,
    )


def attach_status(assignments, student):
    """Set .my_submission, .latest_submission, .my_status, .status_label, .status_badge and .due_soon on each one.

    .my_submission is the student's counted (best) submission and the status
    follows it; .latest_submission is the newest one, which the editor reloads.
    With no submission, the assignment is "todo" while it is open and "missed"
    once it is closed or past its deadline.
    """
    now = timezone.now()
    assignments = list(assignments)
    by_assignment = {}
    for submission in Submission.objects.filter(
        student=student, assignment__in=assignments
    ).order_by("-submitted_at"):
        by_assignment.setdefault(submission.assignment_id, []).append(submission)

    for assignment in assignments:
        attempts = by_assignment.get(assignment.id, [])
        submission = best_submission(attempts)
        if submission:
            status = submission.status  # "submitted" or "graded"
        else:
            status = "todo" if is_open(assignment, now) else "missed"
        assignment.my_submission = submission
        assignment.latest_submission = attempts[0] if attempts else None
        assignment.my_status = status
        assignment.status_label, assignment.status_badge = STATUSES[status]
        assignment.is_open = is_open(assignment, now)
        assignment.due_soon = (
            status == "todo" and assignment.deadline is not None
            and assignment.deadline - now <= DUE_SOON
        )
    return assignments


@student_required
def dashboard(request):
    student = request.user

    # Filter by id in a subquery so the count covers every member, not just this student.
    groups = (
        StudyGroup.objects.filter(id__in=student.study_groups.values("id"))
        .select_related("professor")
        .annotate(student_count=Count("students", distinct=True))
        .order_by("name")
    )
    pending = [
        a
        for a in attach_status(my_assignments(student).order_by("deadline"), student)
        if a.my_status == "todo"
    ]
    graded = (
        Submission.objects.filter(student=student, status=Submission.Status.GRADED)
        .select_related("bug", "assignment")
        .order_by("-graded_at", "-submitted_at")
    )

    return render(
        request,
        "student/dashboard.html",
        {
            "groups": groups,
            "pending": pending[:DASHBOARD_LIMIT],
            "pending_count": len(pending),
            "pending_more": max(len(pending) - DASHBOARD_LIMIT, 0),
            "recent_grades": graded[:DASHBOARD_LIMIT],
            "graded_count": graded.count(),
        },
    )


@student_required
def assignments_list(request):
    assignments = attach_status(my_assignments(request.user).order_by("deadline"), request.user)

    counts = {key: 0 for key in STATUSES}
    for assignment in assignments:
        counts[assignment.my_status] += 1
    tabs = [{"key": "", "label": "All", "count": len(assignments)}] + [
        {"key": key, "label": label, "count": counts[key]} for key, (label, _) in STATUSES.items()
    ]

    current = request.GET.get("status", "")
    if current in STATUSES:
        assignments = [a for a in assignments if a.my_status == current]
    else:
        current = ""

    return render(
        request,
        "student/assignments_list.html",
        {"assignments": assignments, "tabs": tabs, "current": current},
    )


@student_required
def assignment_detail(request, pk):
    # 404 (not 403) for assignments outside the student's groups, so ids leak nothing.
    assignment = get_object_or_404(my_assignments(request.user), pk=pk)
    attach_status([assignment], request.user)
    return render(
        request,
        "student/assignment_detail.html",
        {
            "assignment": assignment,
            "bug": assignment.bug,
            "my_groups": assignment.groups.filter(students=request.user).order_by("name"),
            "submissions": assignment.submissions.filter(student=request.user).order_by(
                "-submitted_at"
            ),
        },
    )


def submit_blocked_reason(assignment):
    """Why the student cannot submit to this assignment now, or None if they can.

    Expects attach_status() to have run. Resubmitting is allowed until the
    deadline, but not once the professor has graded the work.
    """
    if not assignment.is_open:
        return "The deadline has passed, so this assignment no longer accepts submissions."
    if assignment.my_status == "graded":
        return "Your submission is already graded, so it can no longer be changed."
    return None


def workspace(request, bug, *, assignment=None, latest=None, blocked=None):
    """The bug's page: its brief, and a button that opens it in the student's VS Code.

    GET shows the page. POST writes the student's folder, starts their VS Code
    container and redirects there. Submissions come back through ide_submit().
    Shared by assignment work (`assignment` set) and practice (`assignment` None).
    """
    if request.method == "POST":
        if blocked:
            messages.error(request, blocked)
            return redirect(request.path)
        port = int(request.get_port())
        try:
            folder = write_workspace(
                request.user, bug, assignment=assignment,
                start_code=latest.submitted_code if latest else bug.buggy_code,
                site_url=request.build_absolute_uri(request.path),
                server_url=ide_server_url(port),
            )
            # Development on Linux: let the container reach this server (see core/bridge.py).
            ensure_relay(port)
            return redirect(start_ide(request.user, folder))
        except IdeError as error:
            messages.error(request, str(error))
            return redirect(request.path)

    return render(
        request,
        "student/bug_workspace.html",
        {
            "assignment": assignment,
            "bug": bug,
            "blocked": blocked,
            "latest": latest,
            "has_tests": has_tests(bug),
            "project_has_tests": project_has_tests(bug),
            "code_file": code_file_name(bug),
        },
    )


@student_required
def assignment_workspace(request, pk):
    assignment = get_object_or_404(my_assignments(request.user), pk=pk)
    attach_status([assignment], request.user)
    return workspace(
        request,
        assignment.bug,
        assignment=assignment,
        latest=assignment.latest_submission,
        blocked=submit_blocked_reason(assignment),
    )


@csrf_exempt
@require_POST
def ide_submit(request):
    """Save a fix sent by the Debug Gym VS Code extension (authenticated by its token)."""
    scheme, _, key = request.headers.get("Authorization", "").partition(" ")
    token = IdeToken.find(key.strip()) if scheme.lower() == "bearer" and key.strip() else None
    if token is None or not token.student.is_active or not token.student.is_student:
        return JsonResponse(
            {"error": "This VS Code folder is no longer connected. Open it again from the website."}, status=401
        )
    student, bug, assignment = token.student, token.bug, token.assignment

    # Access and deadline rules are the same as on the website.
    if assignment is not None:
        assignment = my_assignments(student).filter(pk=assignment.pk).first()
        if assignment is None:
            return JsonResponse({"error": "You no longer have access to this assignment."}, status=403)
        attach_status([assignment], student)
        blocked = submit_blocked_reason(assignment)
        if blocked:
            return JsonResponse({"error": blocked}, status=403)
    elif not practice_bugs_qs(student).filter(pk=bug.pk).exists():
        return JsonResponse({"error": "You no longer have access to this bug."}, status=403)

    try:
        payload = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        payload = None
    code = payload.get("code") if isinstance(payload, dict) else None
    form = SubmissionForm({"code": code if isinstance(code, str) else ""}, bug=bug)
    if not form.is_valid():
        return JsonResponse({"error": " ".join(form.errors["code"])}, status=400)

    code = form.cleaned_data["code"]

    # Test results come only from server-side verification (DEC-037), never from VS Code.
    passed = total = None
    revision = bug.revision
    if project_has_tests(bug):
        try:
            passed, total = verify(bug, code)
        except VerificationBusy as error:
            return JsonResponse({"error": str(error)}, status=503)
        except VerificationError as error:
            return JsonResponse({"error": str(error)}, status=503)

    with transaction.atomic():
        current = Bug.objects.select_for_update().get(pk=bug.pk)
        if current.revision != revision:
            return JsonResponse(
                {"error": "The bug changed while the tests ran. Open it again from the website."}, status=409
            )
        if assignment is not None:
            locked = Assignment.objects.select_for_update().get(pk=assignment.pk)
            if not is_open(locked) or not locked.groups.filter(students=student).exists():
                return JsonResponse(
                    {"error": "The assignment closed or your access changed while the tests ran."}, status=403
                )
        elif not practice_bugs_qs(student).filter(pk=current.pk).exists():
            return JsonResponse({"error": "You no longer have access to this bug."}, status=403)
        Submission.objects.create(
            student=student, bug=current, assignment=assignment, submitted_code=code,
            tests_passed=passed, tests_total=total,
        )

    result = f" Server check: {passed}/{total} tests pass." if total else ""
    if assignment:
        message = f'Fix submitted for "{assignment.title}".{result} You can resubmit until the deadline.'
    else:
        message = f'Practice attempt saved for "{bug.title}".{result} Practice is not graded.'
    return JsonResponse({"message": message, "passed": passed, "total": total}, status=201)


def practice_bugs_qs(student):
    """Bugs a student may practise: every public bug, plus their own private ones."""
    return Bug.objects.filter(Q(visibility=Bug.Visibility.PUBLIC) | Q(created_by=student))


def my_bug_or_404(student, pk):
    """A bug the student created; anyone else's bug is a 404."""
    return get_object_or_404(Bug, pk=pk, created_by=student)


@student_required
def public_bugs(request):
    student = request.user
    bugs = practice_bugs_qs(student).annotate(
        my_attempts=Count("submissions", filter=Q(submissions__student=student, submissions__assignment=None)),
        last_attempt=Max(
            "submissions__submitted_at",
            filter=Q(submissions__student=student, submissions__assignment=None),
        ),
    )

    query = request.GET.get("q", "").strip()
    language = request.GET.get("language", "")
    difficulty = request.GET.get("difficulty", "")
    only_mine = request.GET.get("mine") == "1"
    if query:
        bugs = bugs.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if language:
        bugs = bugs.filter(language__iexact=language)
    if difficulty in Bug.Difficulty.values:
        bugs = bugs.filter(difficulty=difficulty)
    else:
        difficulty = ""
    if only_mine:
        bugs = bugs.filter(created_by=student)

    languages = (
        practice_bugs_qs(student)
        .order_by(Lower("language"))
        .values_list(Lower("language"), flat=True)
        .distinct()
    )
    return render(
        request,
        "student/public_bugs.html",
        {
            "bugs": bugs.select_related("created_by").order_by("title"),
            "languages": languages,
            "difficulties": Bug.Difficulty.choices,
            "filters": {"q": query, "language": language.lower(), "difficulty": difficulty, "mine": only_mine},
            "filtered": bool(query or language or difficulty or only_mine),
            "my_bug_count": Bug.objects.filter(created_by=student).count(),
        },
    )


@student_required
def practice_workspace(request, pk):
    # Public bugs and the student's own bugs. Other private bugs are reachable
    # only through their assignment.
    bug = get_object_or_404(practice_bugs_qs(request.user), pk=pk)
    latest = (
        Submission.objects.filter(student=request.user, bug=bug, assignment=None)
        .order_by("-submitted_at")
        .first()
    )
    return workspace(request, bug, latest=latest)


@student_required
@sensitive_post_parameters("api_key")
def bug_create(request):
    """New practice bug: the student describes it and an AI writes it."""
    form = AIBugForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        try:
            generated = ai.generate_bug(
                provider=data["provider"],
                api_key=data["api_key"],
                prompt=data["prompt"],
                language=data["language"],
                difficulty=data["difficulty"],
                model=data["model"],
            )
        except ai.AIError as error:
            form.add_error(None, str(error))
        else:
            files, entry = build_project(data["language"], generated["buggy_code"], generated.get("tests_code", ""))
            bug = Bug.objects.create(
                title=generated["title"],
                description=generated["description"],
                buggy_code=generated["buggy_code"],
                solution_code=generated["solution_code"],
                project_files=files,
                entry_file=entry,
                language=data["language"],
                difficulty=data["difficulty"],
                visibility=data["visibility"],
                created_by=request.user,
            )
            messages.success(
                request,
                f'AI created "{bug.title}". AI can make mistakes: check it with "Edit my bug" if something looks off.',
            )
            return redirect("student:practice_workspace", pk=bug.pk)
    return render(request, "student/bug_ai_form.html", {"form": form})


@student_required
def bug_edit(request, pk):
    bug = my_bug_or_404(request.user, pk)
    form = StudentBugForm(request.POST or None, instance=bug)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Bug updated.")
        return redirect("student:practice_workspace", pk=bug.pk)
    return render(request, "student/bug_form.html", {"form": form, "bug": bug})


@student_required
def bug_delete(request, pk):
    bug = my_bug_or_404(request.user, pk)
    if bug.assignments.exists():
        messages.error(
            request, "A professor uses this bug in an assignment, so it can no longer be deleted."
        )
        return redirect("student:bug_edit", pk=bug.pk)
    if request.method == "POST":
        title = bug.title
        bug.delete()  # its practice attempts are deleted with it
        messages.success(request, f"Bug \"{title}\" deleted.")
        return redirect("student:public_bugs")
    return render(
        request,
        "student/bug_confirm_delete.html",
        {
            "bug": bug,
            "attempt_count": bug.submissions.count(),
            "other_students": bug.submissions.exclude(student=request.user)
            .values("student")
            .distinct()
            .count(),
        },
    )


@student_required
def results(request):
    mine = Submission.objects.filter(student=request.user).select_related("bug", "assignment")
    graded = mine.filter(status=Submission.Status.GRADED).order_by("-graded_at", "-submitted_at")
    history = Paginator(mine.order_by("-submitted_at"), HISTORY_PAGE_SIZE).get_page(
        request.GET.get("page")
    )
    return render(
        request,
        "student/results.html",
        {
            "graded": graded,
            "average": graded.aggregate(avg=Avg("grade"))["avg"],
            "waiting_count": mine.filter(
                status=Submission.Status.SUBMITTED, assignment__isnull=False
            ).count(),
            "practice_count": mine.filter(assignment__isnull=True).count(),
            "history": history,
        },
    )


@student_required
@never_cache
def progress(request, pk):
    assignment_pk = request.GET.get("assignment")
    if assignment_pk:
        if not assignment_pk.isdecimal() or len(assignment_pk) > 18:
            return JsonResponse({"error": "Invalid assignment."}, status=400)
        assignment = get_object_or_404(my_assignments(request.user), pk=assignment_pk, bug_id=pk)
        bug = assignment.bug
    else:
        assignment = None
        bug = get_object_or_404(practice_bugs_qs(request.user), pk=pk)
    latest = Submission.objects.filter(
        student=request.user, bug=bug, assignment=assignment,
    ).order_by("-submitted_at", "-pk").first()
    return JsonResponse({
        "id": latest.pk if latest else None,
        "passed": latest.tests_passed if latest else None,
        "total": latest.tests_total if latest else None,
        "submitted": latest.submitted_at.isoformat() if latest else None,
    })
