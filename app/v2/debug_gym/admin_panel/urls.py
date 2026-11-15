# [Admin Dev] URL routes for the admin panel, mounted at /admin-panel/
from django.urls import path

from .views import DashboardView

app_name = "admin_panel"

urlpatterns = [path("", DashboardView.as_view(), name="dashboard")]
