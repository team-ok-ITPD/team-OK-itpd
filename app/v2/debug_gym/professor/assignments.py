# [Professor Dev] Shared atomic assignment flow for group pages and catalog dialogs
from copy import deepcopy

from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse

from core.models import Assignment, Bug, StudyGroup
from .forms import accessible_bugs


@transaction.atomic
def assign_exercise(request, group_pk, assignment):
    group = get_object_or_404(StudyGroup.objects.select_for_update(), pk=group_pk, professor=request.user)
    source = get_object_or_404(accessible_bugs(request.user).select_for_update(), pk=assignment.bug_id)
    if source.created_by_id != request.user.pk:
        source_url = request.build_absolute_uri(reverse("professor:bug", args=[source.pk]))
        assignment.bug = Bug.objects.create(
            title=source.title, description=f"{source.description}\n\nCopied from: {source_url}",
            buggy_code=source.buggy_code, language=source.language, difficulty=source.difficulty,
            project_files=deepcopy(source.project_files), compose_config=source.compose_config,
            dockerfile_config=source.dockerfile_config,
            entry_file=source.entry_file, tests_code=source.tests_code,
            visibility=Bug.Visibility.PRIVATE, created_by=request.user,
        )
    assignment.professor = request.user
    existing = Assignment.objects.select_for_update().filter(
        bug=assignment.bug, professor=request.user, groups=group, is_withdrawn=False,
    ).order_by("pk").first()
    if existing:
        if existing.status == Assignment.Status.CLOSED or getattr(existing, "agent_review", None):
            raise ValidationError("This exercise is already assigned and closed or reviewed. Unassign it before creating a new assignment.")
        existing.title, existing.instructions, existing.deadline = assignment.title, assignment.instructions, assignment.deadline
        existing.save(update_fields=("title", "instructions", "deadline", "updated_at"))
        return existing
    assignment.save()
    assignment.groups.add(group)
    return assignment
