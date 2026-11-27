# [Professor Dev] Views for professor pages: groups, bugs, assignments, grading
from django.views.generic import TemplateView
import csv

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Count
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.conf import settings

from core.models import AgentCredential, Assignment, Bug, StudyGroup, Submission, User
from core.permissions import RoleRequiredMixin, professor_required
from core.agents import AgentError, save_key
from core.runtime import RuntimeError
from app.adel_b.bugs.verification import VerificationBusy

from .forms import (
    AssignmentForm, CatalogAssignmentForm, DeadlineForm, ExerciseDetailsForm, ExerciseForm,
    GenerateForm, KeyForm, accessible_bugs,
)
from .agent_tasks import generate
from .assignments import assign_exercise


class DashboardView(RoleRequiredMixin, TemplateView):
    required_role = User.Role.PROFESSOR
    template_name = "professor/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["groups"] = StudyGroup.objects.filter(
            professor=self.request.user,
        ).annotate(student_count=Count("students", distinct=True))
        context["student_count"] = User.objects.filter(
            study_groups__professor=self.request.user,
        ).distinct().count()
        context["exercise_count"] = Bug.objects.filter(created_by=self.request.user).count()
        return context


def owned_group(user, pk):
    try:
        pk = int(pk)
    except (TypeError, ValueError):
        raise Http404("Group not found.")
    if not 0 < pk < 2**63:
        raise Http404("Group not found.")
    return get_object_or_404(StudyGroup, pk=pk, professor=user)


def owned_assignment(user, group, pk):
    return get_object_or_404(Assignment, pk=pk, groups=group, professor=user)


@professor_required
def group_detail(request, pk):
    group = owned_group(request.user, pk)
    return render(request, "professor/group_detail.html", {
        "group": group,
        "students": group.students.order_by("name", "email"),
        "assignments": group.assignments.filter(professor=request.user, is_withdrawn=False).select_related("bug"),
        "archived_assignments": group.assignments.filter(professor=request.user, is_withdrawn=True).select_related("bug"),
    })


@professor_required
def assign(request, pk):
    group = owned_group(request.user, pk)
    form = AssignmentForm(
        request.POST if request.method == "POST" else None, professor=request.user,
        initial={"bug": request.GET.get("bug")},
    )
    if request.method == "POST" and form.is_valid():
        try:
            assign_exercise(request, pk, form.save(commit=False))
        except ValidationError as error:
            form.add_error(None, error)
        else:
            messages.success(request, "Exercise assigned to the group.")
            return redirect("professor:group", pk=group.pk)
    return render(request, "professor/assignment_form.html", {"group": group, "form": form})


@professor_required
@never_cache
def assignment_detail(request, group_pk, pk):
    group = owned_group(request.user, group_pk)
    assignment = owned_assignment(request.user, group, pk)
    form = DeadlineForm(
        request.POST if request.method == "POST" else None, instance=assignment,
    )
    if request.method == "POST":
        # Older assignments can have several groups sharing one deadline.
        if assignment.is_withdrawn:
            form.add_error(None, "This assignment has been withdrawn and archived.")
        elif getattr(assignment, "agent_review", None):
            form.add_error(None, "The one-time review has started. Create a new assignment to change its deadline.")
        elif assignment.groups.count() != 1:
            form.add_error(None, "This older assignment shares a deadline across groups.")
        elif form.is_valid():
            form.save()
            messages.success(request, "Deadline updated.")
            return redirect("professor:assignment", group_pk=group.pk, pk=pk)
    rows = result_rows(assignment, group) if assignment.results_visible else []
    review = getattr(assignment, "agent_review", None)
    return render(request, "professor/assignment_detail.html", {
        "assignment": assignment, "group": group, "form": form, "rows": rows, "review": review,
    })


@professor_required
def close_assignment(request, group_pk, pk):
    group = owned_group(request.user, group_pk)
    assignment = owned_assignment(request.user, group, pk)
    if request.method != "POST" or request.POST.get("confirm") != "yes":
        return render(request, "professor/assignment_confirm.html", {
            "assignment": assignment, "group": group, "action": "close",
        })
    if assignment.groups.count() != 1:
        messages.error(request, "This older assignment is shared with several groups.")
    else:
        assignment.status = Assignment.Status.CLOSED
        assignment.save(update_fields=("status", "updated_at"))
        messages.success(request, "Assignment closed. Results are now available.")
    return redirect("professor:assignment", group_pk=group.pk, pk=pk)


@professor_required
def unassign(request, group_pk, pk):
    group = owned_group(request.user, group_pk)
    with transaction.atomic():
        assignment = get_object_or_404(
            Assignment.objects.select_for_update(), pk=pk, groups=group, professor=request.user,
        )
        if request.method != "POST" or request.POST.get("confirm") != "yes":
            return render(request, "professor/assignment_confirm.html", {
                "assignment": assignment, "group": group, "action": "unassign",
            })
        if assignment.groups.count() != 1:
            raise Http404("Split this legacy assignment into individual groups first.")
        assignment.is_withdrawn = True
        assignment.status = Assignment.Status.CLOSED
        assignment.save(update_fields=("is_withdrawn", "status", "updated_at"))
    messages.success(request, "Assignment withdrawn. Its submissions and results are retained in the archive.")
    return redirect("professor:group", pk=group.pk)


def result_rows(assignment, group):
    submissions = Submission.objects.filter(
        assignment=assignment, bug=assignment.bug, student__study_groups=group,
    ).order_by("-submitted_at", "-pk")
    best = {}
    flagged = {}
    for submission in submissions:
        if submission.suspicion_status == "review":
            flagged.setdefault(submission.student_id, submission)
        previous = best.get(submission.student_id)
        score = submission.tests_passed
        if previous is None or (
            score is not None
            and (previous.tests_passed is None or score > previous.tests_passed)
        ):
            best[submission.student_id] = submission
    return [
        {
            "student": student, "submission": best.get(student.pk),
            "review": flagged.get(student.pk) or best.get(student.pk),
        }
        for student in group.students.order_by("name", "email")
    ]


def csv_value(value):
    text = str(value)
    # Names and emails are untrusted spreadsheet input.
    return "'" + text if text.lstrip().startswith(("=", "+", "-", "@")) else text


@professor_required
def export_results(request, group_pk, pk):
    group = owned_group(request.user, group_pk)
    assignment = owned_assignment(request.user, group, pk)
    if not assignment.results_visible:
        return HttpResponse("Results are available after the deadline or manual closure.", status=403)
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="assignment-{pk}-group-{group.pk}.csv"'
    response["Cache-Control"] = "no-store"
    response.write("\ufeff")
    writer = csv.writer(response)
    writer.writerow(("Name", "Email", "Tests passed", "Tests total", "Verification", "Suspicion review", "Review notes"))
    for row in result_rows(assignment, group):
        submission = row["submission"]
        review = row["review"]
        checked = submission is not None and submission.tests_passed is not None
        writer.writerow((
            csv_value(row["student"].name), csv_value(row["student"].email),
            submission.tests_passed if checked else "",
            submission.tests_total if checked else "",
            "Verified" if checked else "Awaiting verification" if submission else "No submission",
            review.suspicion_status if review and review.reviewed_at else "Not checked",
            csv_value(review.suspicion_reason) if review else "",
        ))
    return response


@professor_required
def catalog(request):
    bugs = accessible_bugs(request.user).select_related("created_by")
    scope = request.GET.get("scope", "all")
    visibility = request.GET.get("visibility", scope if scope in ("private", "public") else "all")
    owner = request.GET.get("owner", "my" if scope == "mine" else "all")
    if visibility not in ("all", "public", "private"):
        visibility = "all"
    if owner not in ("all", "my", "others"):
        owner = "all"
    if visibility != "all":
        bugs = bugs.filter(visibility=visibility)
    if owner == "my":
        bugs = bugs.filter(created_by=request.user)
    elif owner == "others":
        bugs = bugs.exclude(created_by=request.user)
    query = request.GET.get("q", "").strip()
    if query:
        bugs = bugs.filter(title__icontains=query)
    group = owned_group(request.user, request.GET["group"]) if request.GET.get("group") else None
    template = "professor/catalog_cards.html" if request.GET.get("fragment") == "1" else "professor/bugs_list.html"
    return render(request, template, {
        "bugs": bugs.order_by("title"), "query": query, "visibility": visibility, "owner": owner, "group": group,
        "groups": StudyGroup.objects.filter(professor=request.user).order_by("name", "group_number"),
    })


@professor_required
@require_POST
def catalog_assign(request, pk):
    bug = get_object_or_404(accessible_bugs(request.user), pk=pk)
    form = CatalogAssignmentForm(request.POST, professor=request.user)
    if not form.is_valid():
        return JsonResponse({"error": " ".join(message for errors in form.errors.values() for message in errors)}, status=400)
    group = form.cleaned_data["group"]
    try:
        assign_exercise(request, group.pk, Assignment(
            bug=bug, title=bug.title, deadline=form.cleaned_data["deadline"],
        ))
    except ValidationError as error:
        return JsonResponse({"error": " ".join(error.messages)}, status=400)
    messages.success(request, "Exercise assigned to the group.")
    return JsonResponse({"redirect": reverse("professor:group", args=[group.pk])})


@professor_required
@require_POST
def publish(request, pk):
    bug = get_object_or_404(Bug, pk=pk, created_by=request.user)
    bug.visibility = Bug.Visibility.PUBLIC
    bug.save(update_fields=("visibility", "updated_at"))
    messages.success(request, "Exercise published.")
    return redirect("professor:bugs")


@professor_required
@require_POST
def unpublish(request, pk):
    bug = get_object_or_404(Bug, pk=pk, created_by=request.user)
    bug.visibility = Bug.Visibility.PRIVATE
    bug.save(update_fields=("visibility", "updated_at"))
    messages.success(request, "Exercise unpublished. Existing assignments are unchanged.")
    return redirect("professor:bugs")


@professor_required
def create_exercise(request):
    group_id = request.GET.get("group") or request.POST.get("group")
    group = owned_group(request.user, group_id) if group_id else None
    form = ExerciseForm(
        request.POST if request.method == "POST" else None, request.FILES or None,
    )
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            if group:
                group = get_object_or_404(
                    StudyGroup.objects.select_for_update(),
                    pk=group.pk, professor=request.user,
                )
            bug = form.save(commit=False)
            bug.created_by = request.user
            bug.visibility = Bug.Visibility.PRIVATE
            bug.project_files = form.cleaned_data["project"]
            bug.entry_file = form.cleaned_data["entry_file"]
            bug.buggy_code = bug.project_files[form.cleaned_data["entry_file"]]
            bug.dockerfile_config = form.cleaned_data["dockerfile"]
            bug.save()
            if group:
                assignment = Assignment.objects.create(
                    title=bug.title, bug=bug, professor=request.user,
                )
                assignment.groups.add(group)
        messages.success(request, "Private exercise created." + (" Assigned to the group." if group else ""))
        return redirect("professor:group", pk=group.pk) if group else redirect("professor:bugs")
    return render(request, "professor/bug_form.html", {
        "form": form, "group": group, "generate_form": GenerateForm(),
    })


@professor_required
@sensitive_post_parameters("key")
def settings_page(request):
    credential = AgentCredential.objects.filter(user=request.user).first()
    form = KeyForm(request.POST if request.method == "POST" else None,
                   initial={"provider": credential.provider if credential else "openai"})
    if request.method == "POST" and form.is_valid():
        save_key(request.user, form.cleaned_data["key"], form.cleaned_data["provider"])
        messages.success(request, "Generation credentials updated.")
        return redirect("professor:settings")
    return render(request, "professor/settings.html", {
        "form": form,
        "has_key": AgentCredential.objects.filter(user=request.user).exists(),
        "platform_key": bool(settings.DEBUG_GYM_AGENT_KEY),
    })


@professor_required
def bug_detail(request, pk):
    bug = get_object_or_404(accessible_bugs(request.user), pk=pk)
    can_edit = bug.created_by_id == request.user.pk
    form = ExerciseDetailsForm(
        request.POST if request.method == "POST" else None, instance=bug,
    )
    if request.method == "POST":
        if not can_edit:
            raise Http404()
        if form.is_valid():
            with transaction.atomic():
                current = Bug.objects.select_for_update().get(pk=pk)
                if request.POST.get("revision") != str(current.revision):
                    form.add_error(None, "The exercise changed. Reload before saving.")
                else:
                    updated = form.save(commit=False)
                    updated.revision = current.revision + 1
                    updated.save(update_fields=("title", "description", "difficulty", "revision", "updated_at"))
                    messages.success(request, "Exercise details saved.")
                    return redirect("professor:bug", pk=pk)
    return render(request, "professor/bug_detail.html", {
        "bug": bug, "form": form, "can_edit": can_edit,
        "groups": StudyGroup.objects.filter(professor=request.user).order_by("name", "group_number"),
    })


@professor_required
@require_POST
def generate_exercise(request):
    group_id = request.POST.get("group")
    group = owned_group(request.user, group_id) if group_id else None
    form = GenerateForm(request.POST)
    if form.is_valid():
        try:
            bug = generate(
                request.user, form.cleaned_data["prompt"],
                form.cleaned_data["language"], form.cleaned_data["test_count"],
            )
            with transaction.atomic():
                if group:
                    group = get_object_or_404(
                        StudyGroup.objects.select_for_update(), pk=group.pk, professor=request.user,
                    )
                bug.save()
                if group:
                    assignment = Assignment.objects.create(
                        title=bug.title, bug=bug, professor=request.user,
                    )
                    assignment.groups.add(group)
            messages.success(request, "Exercise generated and its tests verified.")
            return redirect("professor:group", pk=group.pk) if group else redirect("professor:bug", pk=bug.pk)
        except (AgentError, RuntimeError, VerificationBusy) as error:
            form.add_error(None, str(error))
    return render(request, "professor/bug_form.html", {
        "form": ExerciseForm(), "generate_form": form, "group": group, "active_tab": "generate",
    })
