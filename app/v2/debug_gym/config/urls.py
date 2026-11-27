# [Backend Dev] Main URL routes, includes each app's urls with its prefix
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from core import workspace_api

urlpatterns = [
    path("api/workspaces/<int:pk>/", workspace_api.launch, name="workspace-launch"),
    path("api/ide/pair/", workspace_api.pair, name="ide-pair"),
    path("api/ide/submit/", workspace_api.submit, name="ide-submit"),
    # Site root: send visitors to login until role dashboards exist
    path("", RedirectView.as_view(url="/accounts/login/", permanent=False), name="home"),
    # Built-in Django admin (kept separate from our own /admin-panel/)
    path("django-admin/", admin.site.urls),
    # Debug Gym apps, one prefix per role
    path("accounts/", include("accounts.urls")),
    path("admin-panel/", include("admin_panel.urls")),
    path("professor/", include("professor.urls")),
    path("student/", include("student.urls")),
]
