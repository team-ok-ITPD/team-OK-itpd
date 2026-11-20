# [Admin Dev] Views for administrator-managed teacher accounts and group membership
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView

from core.models import Assignment, GroupStudent, StudyGroup, User
from core.permissions import RoleRequiredMixin

from .forms import GroupMemberForm, TeacherForm


class DashboardView(RoleRequiredMixin, TemplateView):
    required_role = User.Role.ADMIN
    template_name = "admin_panel/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["teacher_count"] = User.objects.filter(role=User.Role.PROFESSOR).count()
        context["student_count"] = User.objects.filter(role=User.Role.STUDENT).count()
        context["group_count"] = StudyGroup.objects.count()
        context["assignment_count"] = Assignment.objects.filter(
            status=Assignment.Status.ACTIVE
        ).count()
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["creating"] = True
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Teacher account created.")
        return super().form_valid(form)


class TeacherUpdateView(RoleRequiredMixin, UpdateView):
    required_role = User.Role.ADMIN
    form_class = TeacherForm
    template_name = "admin_panel/user_form.html"
    success_url = reverse_lazy("admin_panel:users")

    def get_queryset(self):
        return User.objects.filter(role=User.Role.PROFESSOR)

    def form_valid(self, form):
        messages.success(self.request, "Teacher account updated.")
        return super().form_valid(form)


class GroupListView(RoleRequiredMixin, ListView):
    required_role = User.Role.ADMIN
    context_object_name = "groups"
    template_name = "admin_panel/groups_list.html"
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        queryset = StudyGroup.objects.select_related("professor").prefetch_related("students")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(professor__name__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "").strip()
        return context


class GroupDetailView(RoleRequiredMixin, DetailView):
    required_role = User.Role.ADMIN
    context_object_name = "group"
    template_name = "admin_panel/group_students.html"
    queryset = StudyGroup.objects.select_related("professor").prefetch_related("students")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["member_form"] = GroupMemberForm(group=self.object)
        return context


class GroupMemberAddView(RoleRequiredMixin, View):
    required_role = User.Role.ADMIN

    def post(self, request, pk):
        group = get_object_or_404(StudyGroup, pk=pk)
        form = GroupMemberForm(request.POST, group=group)
        if form.is_valid():
            try:
                with transaction.atomic():
                    GroupStudent.objects.create(
                        group=group,
                        student=form.cleaned_data["student"],
                    )
            except IntegrityError:
                messages.error(request, "This student is already in the group.")
            else:
                messages.success(request, "Student added to the group.")
        else:
            group = StudyGroup.objects.select_related("professor").prefetch_related("students").get(pk=group.pk)
            return render(
                request,
                "admin_panel/group_students.html",
                {"group": group, "member_form": form},
                status=400,
            )
        return HttpResponseRedirect(reverse("admin_panel:group-detail", kwargs={"pk": group.pk}))


class GroupMemberRemoveView(RoleRequiredMixin, View):
    required_role = User.Role.ADMIN

    def post(self, request, pk, student_pk):
        group = get_object_or_404(StudyGroup, pk=pk)
        membership = get_object_or_404(GroupStudent, group=group, student_id=student_pk)
        membership.delete()
        messages.success(request, "Student removed from the group.")
        return HttpResponseRedirect(reverse("admin_panel:group-detail", kwargs={"pk": group.pk}))


class AssignmentListView(RoleRequiredMixin, ListView):
    required_role = User.Role.ADMIN
    context_object_name = "assignments"
    template_name = "admin_panel/assignments_list.html"
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        queryset = Assignment.objects.select_related("bug", "professor").prefetch_related("groups")
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(bug__title__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "").strip()
        return context


class AssignmentDetailView(RoleRequiredMixin, DetailView):
    required_role = User.Role.ADMIN
    context_object_name = "assignment"
    template_name = "admin_panel/assignment_detail.html"
    queryset = Assignment.objects.select_related("bug", "professor").prefetch_related("groups")
