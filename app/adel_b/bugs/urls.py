from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/exercises", views.exercise_match, name="exercise-match"),
    path("health", views.health, name="health"),
    path("api/bugs/", views.bug_list, name="bug-list"),
    path("api/bugs/<slug:slug>/", views.bug_detail, name="bug-detail"),
    path("api/bugs/<slug:slug>/draft/", views.bug_draft, name="bug-draft"),
    path("api/bugs/<slug:slug>/attempts/", views.bug_attempts, name="bug-attempts"),
    path("api/bugs/<slug:slug>/tests/<int:index>/", views.bug_test, name="bug-test"),
    path("api/bugs/<slug:slug>/vscode/", views.bug_vscode, name="bug-vscode"),
    path("api/history/", views.history, name="history"),
    path("api/ide/submit/", views.ide_submit, name="ide-submit"),
]
