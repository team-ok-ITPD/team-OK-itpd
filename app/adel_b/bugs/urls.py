from django.urls import path

from . import teaching, views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/exercises", views.exercise_match, name="exercise-match"),
    path("health", views.health, name="health"),
    path("api/bugs/", views.bug_list, name="bug-list"),
    path("api/bugs/<slug:slug>/", views.bug_detail, name="bug-detail"),
    path("api/bugs/<slug:slug>/progress/", views.bug_progress, name="bug-progress"),
    path("api/bugs/<slug:slug>/draft/", views.bug_draft, name="bug-draft"),
    path("api/bugs/<slug:slug>/attempts/", views.bug_attempts, name="bug-attempts"),
    path("api/bugs/<slug:slug>/tests/<int:index>/", views.bug_test, name="bug-test"),
    path("api/bugs/<slug:slug>/vscode/", views.bug_vscode, name="bug-vscode"),
    path("api/history/", views.history, name="history"),
    path("api/ide/submit/", views.ide_submit, name="ide-submit"),
    path("api/teach/exercises/", teaching.exercises, name="teach-exercises"),
    path("api/teach/exercises/<slug:slug>/", teaching.exercise, name="teach-exercise"),
    path("api/teach/exercises/<slug:slug>/assignments/", teaching.assignments, name="teach-assignments"),
    path(
        "api/teach/exercises/<slug:slug>/assignments/<int:student_id>/",
        teaching.unassign,
        name="teach-unassign",
    ),
    path("api/teach/students/", teaching.students, name="teach-students"),
    path("api/assignments/", teaching.my_assignments, name="my-assignments"),
]
