# [Professor Dev] One provider attempt for all submissions after the deadline
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from core.agents import AgentError, api_key
from core.models import Assignment, AssignmentReview, Submission
from .agent_tasks import analyze


def run_review(assignment):
    if not assignment.results_visible:
        return "waiting"
    existing = AssignmentReview.objects.filter(assignment=assignment).first()
    if existing:
        return existing.status
    # No provider request is attempted until a key exists.
    api_key(assignment.professor)
    with transaction.atomic():
        assignment = Assignment.objects.select_for_update().select_related(
            "professor", "bug",
        ).get(pk=assignment.pk)
        if not assignment.results_visible:
            return "waiting"
        review, created = AssignmentReview.objects.get_or_create(assignment=assignment)
        if not created:
            return review.status
    submissions = list(assignment.submissions.filter(bug=assignment.bug).order_by("pk"))
    try:
        findings = analyze(assignment.professor, assignment.bug, submissions) if submissions else {}
        with transaction.atomic():
            for submission in submissions:
                flagged, reason = findings[submission.pk]
                Submission.objects.filter(pk=submission.pk).update(
                    suspicion_status="review" if flagged else "clear",
                    suspicion_reason=reason, reviewed_at=timezone.now(),
                )
            review.status = "completed"
            review.finished_at = timezone.now()
            review.detail = f"Reviewed {len(submissions)} submissions."
            review.save()
    except AgentError as error:
        review.status = "failed"
        review.finished_at = timezone.now()
        review.detail = str(error)
        review.save()
    return review.status


def review_due_assignments():
    due = Assignment.objects.filter(
        Q(deadline__lte=timezone.now()) | Q(status=Assignment.Status.CLOSED),
        agent_review__isnull=True,
    ).select_related("professor", "bug")
    for assignment in due:
        try:
            run_review(assignment)
        except AgentError:
            # An unconfigured credential keeps the assignment pending.
            continue
