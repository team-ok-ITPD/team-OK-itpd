# [Professor Dev] URL routes for the professor app, mounted at /professor/
from django.urls import path

from . import views

app_name = "professor"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("groups/<int:pk>/", views.group_detail, name="group"),
    path("groups/<int:pk>/assign/", views.assign, name="assign"),
    path("groups/<int:group_pk>/assignments/<int:pk>/", views.assignment_detail, name="assignment"),
    path("groups/<int:group_pk>/assignments/<int:pk>/close/", views.close_assignment, name="close"),
    path("groups/<int:group_pk>/assignments/<int:pk>/unassign/", views.unassign, name="unassign"),
    path("groups/<int:group_pk>/assignments/<int:pk>/export/", views.export_results, name="export"),
    path("bugs/", views.catalog, name="bugs"),
    path("bugs/new/", views.create_exercise, name="create"),
    path("bugs/generate/", views.generate_exercise, name="generate"),
    path("bugs/<int:pk>/", views.bug_detail, name="bug"),
    path("bugs/<int:pk>/assign/", views.catalog_assign, name="catalog-assign"),
    path("settings/", views.settings_page, name="settings"),
    path("bugs/<int:pk>/publish/", views.publish, name="publish"),
    path("bugs/<int:pk>/unpublish/", views.unpublish, name="unpublish"),
]
