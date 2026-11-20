# [Admin Dev] URL routes for the admin panel, mounted at /admin-panel/
from django.urls import path

from .views import AssignmentDetailView, AssignmentListView, DashboardView, GroupDetailView, GroupListView, GroupMemberAddView, GroupMemberRemoveView, TeacherCreateView, TeacherListView, TeacherUpdateView
from .views import AdministratorCreateView, AdministratorListView, GroupCreateView, GroupUpdateView, ProvisionedAccountListView, StudentCreateView

app_name = "admin_panel"

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("users/", TeacherListView.as_view(), name="users"),
    path("users/new/", TeacherCreateView.as_view(), name="user-create"),
    path("users/<int:pk>/", TeacherUpdateView.as_view(), name="user-edit"),
    path("students/", ProvisionedAccountListView.as_view(), name="students"),
    path("students/new/", StudentCreateView.as_view(), name="student-create"),
    path("administrators/", AdministratorListView.as_view(), name="administrators"),
    path("administrators/new/", AdministratorCreateView.as_view(), name="administrator-create"),
    path("groups/", GroupListView.as_view(), name="groups"),
    path("groups/new/", GroupCreateView.as_view(), name="group-create"),
    path("groups/<int:pk>/edit/", GroupUpdateView.as_view(), name="group-edit"),
    path("groups/<int:pk>/", GroupDetailView.as_view(), name="group-detail"),
    path("groups/<int:pk>/members/", GroupMemberAddView.as_view(), name="group-member-add"),
    path("groups/<int:pk>/members/<int:student_pk>/remove/", GroupMemberRemoveView.as_view(), name="group-member-remove"),
    path("assignments/", AssignmentListView.as_view(), name="assignments"),
    path("assignments/<int:pk>/", AssignmentDetailView.as_view(), name="assignment-detail"),
]
