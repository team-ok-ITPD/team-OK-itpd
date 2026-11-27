# [Admin Dev] Views for administrator-managed teacher accounts and group membership
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from core.models import GroupStudent, StudyGroup, User
from core.permissions import RoleRequiredMixin

from .forms import AdministratorForm, GroupForm, StudentBatchForm, StudentForm, StudentImportForm, TeacherForm
from .imports import import_students
from .mail import send_access_link
from .access import revoke_access


class DashboardView(RoleRequiredMixin, TemplateView):
    required_role = User.Role.ADMIN
    template_name = "admin_panel/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["teacher_count"] = User.objects.filter(role=User.Role.PROFESSOR).count()
        context["student_count"] = User.objects.filter(role=User.Role.STUDENT).count()
        context["group_count"] = StudyGroup.objects.count()
        return context


class TeacherListView(RoleRequiredMixin, ListView):
    required_role = User.Role.ADMIN
    context_object_name = "teachers"
    template_name = "admin_panel/users_list.html"
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        queryset = User.objects.filter(role=User.Role.PROFESSOR)
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(email__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "").strip()
        return context


class TeacherCreateView(RoleRequiredMixin, CreateView):
    required_role = User.Role.ADMIN
    form_class = TeacherForm
    template_name = "admin_panel/user_form.html"
    success_url = reverse_lazy("admin_panel:users")
    account_label = "teacher"
    account_list_url_name = "admin_panel:users"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["creating"] = True
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"{self.account_label.capitalize()} account created.")
        if settings.ACCOUNT_EMAIL_ENABLED and self.object.is_active:
            report_access_delivery(
                self.request, self.object, initial_password=form.cleaned_data.get("password")
            )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account_label"] = self.account_label
        context["account_list_url_name"] = self.account_list_url_name
        return context


class StudentCreateView(TeacherCreateView):
    form_class = StudentForm
    account_label = "student"
    success_url = reverse_lazy("admin_panel:students")
    account_list_url_name = "admin_panel:students"


class AdministratorCreateView(TeacherCreateView):
    form_class = AdministratorForm
    account_label = "administrator"
    success_url = reverse_lazy("admin_panel:administrators")
    account_list_url_name = "admin_panel:administrators"


class ProvisionedAccountListView(RoleRequiredMixin, ListView):
    required_role = User.Role.ADMIN
    template_name = "admin_panel/accounts_list.html"
    context_object_name = "accounts"
    paginate_by = 20
    account_role = User.Role.STUDENT
    account_label = "Student"
    create_url_name = "admin_panel:student-create"
    edit_url_name = "admin_panel:student-edit"
    list_url_name = "admin_panel:students"

    def get_queryset(self):
        queryset = User.objects.filter(role=self.account_role)
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(email__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            account_label=self.account_label,
            create_url_name=self.create_url_name,
            edit_url_name=self.edit_url_name,
            list_url_name=self.list_url_name,
            is_student_list=self.account_role == User.Role.STUDENT,
            query=self.request.GET.get("q", "").strip(),
        )
        return context


class AdministratorListView(ProvisionedAccountListView):
    account_role = User.Role.ADMIN
    account_label = "Administrator"
    create_url_name = "admin_panel:administrator-create"
    edit_url_name = "admin_panel:administrator-edit"
    list_url_name = "admin_panel:administrators"


class StudentListView(ProvisionedAccountListView):
    paginate_by = 30

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related("study_groups__professor")
        group_id = self.request.GET.get("group", "")
        if group_id:
            if not group_id.isdecimal() or len(group_id) > 19:
                return queryset.none()
            group = get_object_or_404(StudyGroup, pk=group_id)
            queryset = queryset.filter(study_groups=group)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["groups"] = StudyGroup.objects.select_related("professor")
        context["selected_group"] = self.request.GET.get("group", "")
        context["student_total"] = context["paginator"].count
        context["batch_form"] = StudentBatchForm()
        context["reset_student_selection"] = self.request.session.pop(
            "reset_student_selection", False
        )
        return context


class TeacherUpdateView(RoleRequiredMixin, UpdateView):
    required_role = User.Role.ADMIN
    form_class = TeacherForm
    template_name = "admin_panel/user_form.html"
    success_url = reverse_lazy("admin_panel:users")
    account_role = User.Role.PROFESSOR
    account_label = "teacher"
    account_list_url_name = "admin_panel:users"

    def get_queryset(self):
        return User.objects.filter(role=self.account_role)

    def form_valid(self, form):
        if form.instance.pk == self.request.user.pk and not form.cleaned_data["is_active"]:
            form.add_error("is_active", "You cannot deactivate your own administrator account.")
            return self.form_invalid(form)
        response = super().form_valid(form)
        if not self.object.is_active:
            revoke_access([self.object])
        if self.object.pk == self.request.user.pk:
            update_session_auth_hash(self.request, self.object)
        if form.cleaned_data.get("password") and settings.ACCOUNT_EMAIL_ENABLED:
            report_access_delivery(self.request, self.object)
        messages.success(self.request, f"{self.account_label.capitalize()} account updated.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account_label"] = self.account_label
        context["account_list_url_name"] = self.account_list_url_name
        context["can_delete"] = self.object.pk != self.request.user.pk
        return context


class StudentUpdateView(TeacherUpdateView):
    form_class = StudentForm
    account_role = User.Role.STUDENT
    account_label = "student"
    success_url = reverse_lazy("admin_panel:students")
    account_list_url_name = "admin_panel:students"


class AdministratorUpdateView(TeacherUpdateView):
    form_class = AdministratorForm
    account_role = User.Role.ADMIN
    account_label = "administrator"
    success_url = reverse_lazy("admin_panel:administrators")
    account_list_url_name = "admin_panel:administrators"


class GroupCreateView(RoleRequiredMixin, CreateView):
    required_role = User.Role.ADMIN
    form_class = GroupForm
    template_name = "admin_panel/group_form.html"

    def get_success_url(self):
        return reverse("admin_panel:groups")

    def form_valid(self, form):
        messages.success(self.request, "Teaching group created.")
        return super().form_valid(form)


class GroupUpdateView(RoleRequiredMixin, UpdateView):
    required_role = User.Role.ADMIN
    model = StudyGroup
    form_class = GroupForm
    template_name = "admin_panel/group_form.html"

    def get_success_url(self):
        return reverse("admin_panel:groups")

    def form_valid(self, form):
        messages.success(self.request, "Teaching group updated.")
        return super().form_valid(form)


class GroupListView(RoleRequiredMixin, ListView):
    required_role = User.Role.ADMIN
    context_object_name = "groups"
    template_name = "admin_panel/groups_list.html"
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        queryset = StudyGroup.objects.select_related("professor")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(professor__name__icontains=query)
                | Q(professor__email__icontains=query) | Q(description__icontains=query)
                | Q(group_number__icontains=query)
                | Q(course__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "").strip()
        return context


class StudentBatchView(RoleRequiredMixin, View):
    required_role = User.Role.ADMIN

    def post(self, request):
        form = StudentBatchForm(request.POST)
        if form.is_valid():
            students = form.cleaned_data["students"]
            action = form.cleaned_data["action"]
            group = form.cleaned_data["group"]
            with transaction.atomic():
                # Lock/recheck activity in the same transaction as enrollment.
                selected = list(students.select_for_update())
                if action == "add":
                    if any(not student.is_active for student in selected):
                        messages.error(request, "Activate all selected students before enrollment.")
                        return redirect("admin_panel:students")
                    for student in selected:
                        GroupStudent.objects.get_or_create(group=group, student=student)
                elif action == "remove":
                    GroupStudent.objects.filter(group=group, student__in=selected).delete()
                else:
                    User.objects.filter(pk__in=[user.pk for user in selected]).update(
                        is_active=action == "activate"
                    )
                    if action == "deactivate":
                        revoke_access(selected)
            messages.success(request, f"Applied {action} to {len(selected)} selected students.")
            request.session["reset_student_selection"] = True
        else:
            return render(request, "admin_panel/batch_errors.html", {"form": form}, status=400)
        url = reverse("admin_panel:students")
        filters = {
            key: request.POST.get(field, "").strip()
            for key, field in (("q", "filter_q"), ("group", "filter_group"), ("page", "filter_page"))
            if request.POST.get(field, "").strip()
        }
        if filters:
            url += "?" + urlencode(filters)
        return redirect(url)


class StudentImportView(RoleRequiredMixin, View):
    required_role = User.Role.ADMIN

    def get(self, request):
        return render(request, "admin_panel/student_import.html", {"form": StudentImportForm()})

    def post(self, request):
        form = StudentImportForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                result, notify = import_students(form.cleaned_data["file"])
            except ValidationError as error:
                form.add_error("file", error)
            except IntegrityError:
                form.add_error("file", "Conflicting records were changed concurrently. No rows were applied; retry.")
            else:
                messages.success(request, (
                    f"CSV applied: {result['created']} created, {result['updated']} updated, "
                    f"{result['groups']} groups created, {result['memberships']} memberships added."
                ))
                if settings.ACCOUNT_EMAIL_ENABLED:
                    sent = sum(
                        send_access_link(user, initial_password=password)
                        for user, password in notify if user.is_active
                    )
                    expected = sum(user.is_active for user, _ in notify)
                    if sent != expected:
                        messages.warning(request, "Some access emails were not sent. Use Send access link after checking mail configuration.")
                return redirect("admin_panel:students")
        return render(request, "admin_panel/student_import.html", {"form": form}, status=400)


def report_access_delivery(request, user, *, initial_password=None):
    if send_access_link(user, initial_password=initial_password):
        if initial_password:
            messages.success(request, "An account email with the initial password and an access link was sent.")
        else:
            messages.success(request, "An access link was emailed. No password was sent.")
    else:
        messages.warning(request, "Access email was not sent. Check email configuration and account activity, then retry.")


class AccountAccessLinkView(RoleRequiredMixin, View):
    required_role = User.Role.ADMIN

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        report_access_delivery(request, user)
        return redirect(account_list_name(user))


def account_list_name(user):
    return {
        User.Role.PROFESSOR: "admin_panel:users",
        User.Role.STUDENT: "admin_panel:students",
        User.Role.ADMIN: "admin_panel:administrators",
    }[user.role]


class AccountDeleteView(RoleRequiredMixin, View):
    required_role = User.Role.ADMIN

    def context(self, request, user):
        # Do not silently erase submitted work through cascading user deletion.
        blocked = (
            user.pk == request.user.pk
            or user.submissions.exists()
            or user.created_bugs.exists()
            or user.created_assignments.exists()
            or user.taught_groups.exists()
        )
        return {
            "account": user, "blocked": blocked,
            "membership_count": user.study_groups.count(),
            "list_url_name": account_list_name(user),
        }

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        return render(request, "admin_panel/account_delete.html", self.context(request, user))

    def post(self, request, pk):
        with transaction.atomic():
            user = get_object_or_404(User.objects.select_for_update(), pk=pk)
            context = self.context(request, user)
            if context["blocked"] or request.POST.get("confirm") != "yes":
                context["error"] = "Deletion blocked or confirmation missing. Deactivate the account to preserve its history."
                return render(request, "admin_panel/account_delete.html", context, status=400)
            destination = account_list_name(user)
            try:
                revoke_access([user])
                user.delete()
            except ProtectedError:
                messages.error(request, "Related teaching data prevents deletion. Deactivate the account instead.")
            else:
                messages.success(request, "Account deleted. Memberships and access tokens were removed.")
        return redirect(destination)
