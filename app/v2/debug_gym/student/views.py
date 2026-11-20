# [Student Dev] Views for student pages: assignments, bug workspace, practice, results
from datetime import timedelta

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Max, Q
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from core.models import Assignment, Bug, StudyGroup, Submission
from core.permissions import student_required

from .forms import SubmissionForm

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
    return assignment.status == Assignment.Status.ACTIVE and assignment.deadline >= now


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
        assignment.due_soon = status == "todo" and assignment.deadline - now <= DUE_SOON
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


def workspace(request, bug, *, assignment=None, latest=None, blocked=None, done_url, done_message):
    """Show the editor for `bug` and save a submission on POST.

    Shared by assignment work (`assignment` set) and practice (`assignment` None,
    never graded). `latest` is the submission whose code fills the editor.
    """
    if request.method == "POST":
        # Checked on the server too: a stale open tab must not submit after the deadline.
        if blocked:
            messages.error(request, blocked)
            return redirect(request.path)
        form = SubmissionForm(request.POST, bug=bug)
        if form.is_valid():
            Submission.objects.create(
                student=request.user,
                bug=bug,
                assignment=assignment,
                submitted_code=form.cleaned_data["code"],
            )
            messages.success(request, done_message)
            return redirect(done_url)
    else:
        form = SubmissionForm(
            bug=bug, initial={"code": latest.submitted_code if latest else bug.buggy_code}
        )

    return render(
        request,
        "student/bug_workspace.html",
        {"assignment": assignment, "bug": bug, "form": form, "blocked": blocked, "latest": latest},
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
        done_url=reverse("student:assignment_detail", args=[assignment.pk]),
        done_message="Fix submitted. You can resubmit until the deadline.",
    )


def public_bugs_qs():
    return Bug.objects.filter(visibility=Bug.Visibility.PUBLIC)


@student_required
def public_bugs(request):
    student = request.user
    bugs = public_bugs_qs().annotate(
        my_attempts=Count("submissions", filter=Q(submissions__student=student, submissions__assignment=None)),
        last_attempt=Max(
            "submissions__submitted_at",
            filter=Q(submissions__student=student, submissions__assignment=None),
        ),
    )

    query = request.GET.get("q", "").strip()
    language = request.GET.get("language", "")
    difficulty = request.GET.get("difficulty", "")
    if query:
        bugs = bugs.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if language:
        bugs = bugs.filter(language__iexact=language)
    if difficulty in Bug.Difficulty.values:
        bugs = bugs.filter(difficulty=difficulty)
    else:
        difficulty = ""

    languages = (
        public_bugs_qs().order_by(Lower("language")).values_list(Lower("language"), flat=True).distinct()
    )
    return render(
        request,
        "student/public_bugs.html",
        {
            "bugs": bugs.order_by("title"),
            "languages": languages,
            "difficulties": Bug.Difficulty.choices,
            "filters": {"q": query, "language": language.lower(), "difficulty": difficulty},
            "filtered": bool(query or language or difficulty),
        },
    )


@student_required
def practice_workspace(request, pk):
    # Only public bugs: a private bug is reachable only through its assignment.
    bug = get_object_or_404(public_bugs_qs(), pk=pk)
    latest = (
        Submission.objects.filter(student=request.user, bug=bug, assignment=None)
        .order_by("-submitted_at")
        .first()
    )
    return workspace(
        request,
        bug,
        latest=latest,
        done_url=reverse("student:practice_workspace", args=[bug.pk]),
        done_message="Practice attempt saved. Practice is not graded.",
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
