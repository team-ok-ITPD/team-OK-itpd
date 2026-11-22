# [Admin Dev] Administrator accounts, groups and centralized student management
from django.urls import path

from . import views

app_name = "admin_panel"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("users/", views.TeacherListView.as_view(), name="users"),
    path("users/new/", views.TeacherCreateView.as_view(), name="user-create"),
    path("users/<int:pk>/", views.TeacherUpdateView.as_view(), name="user-edit"),
    path("students/", views.StudentListView.as_view(), name="students"),
    path("students/new/", views.StudentCreateView.as_view(), name="student-create"),
    path("students/import/", views.StudentImportView.as_view(), name="student-import"),
    path("students/batch/", views.StudentBatchView.as_view(), name="student-batch"),
    path("students/<int:pk>/", views.StudentUpdateView.as_view(), name="student-edit"),
    path("administrators/", views.AdministratorListView.as_view(), name="administrators"),
    path("administrators/new/", views.AdministratorCreateView.as_view(), name="administrator-create"),
    path("administrators/<int:pk>/", views.AdministratorUpdateView.as_view(), name="administrator-edit"),
    path("accounts/<int:pk>/delete/", views.AccountDeleteView.as_view(), name="account-delete"),
    path("accounts/<int:pk>/access-link/", views.AccountAccessLinkView.as_view(), name="account-access-link"),
    path("groups/", views.GroupListView.as_view(), name="groups"),
    path("groups/new/", views.GroupCreateView.as_view(), name="group-create"),
    path("groups/<int:pk>/edit/", views.GroupUpdateView.as_view(), name="group-edit"),
]
