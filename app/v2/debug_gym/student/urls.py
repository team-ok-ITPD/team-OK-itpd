# [Student Dev] URL routes for the student app, mounted at /student/
from django.urls import path

from . import views

app_name = "student"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("assignments/", views.assignments_list, name="assignments_list"),
    path("assignments/<int:pk>/", views.assignment_detail, name="assignment_detail"),
    path("assignments/<int:pk>/solve/", views.assignment_workspace, name="assignment_workspace"),
    path("practice/", views.public_bugs, name="public_bugs"),
    path("practice/new/", views.bug_create, name="bug_create"),
    path("practice/<int:pk>/", views.practice_workspace, name="practice_workspace"),
    path("practice/<int:pk>/edit/", views.bug_edit, name="bug_edit"),
    path("practice/<int:pk>/delete/", views.bug_delete, name="bug_delete"),
    path("results/", views.results, name="results"),
    path("progress/<int:pk>/", views.progress, name="progress"),
    # Called by the student's Debug Gym VS Code extension, not by the browser.
    path("ide/submit/", views.ide_submit, name="ide_submit"),
]
