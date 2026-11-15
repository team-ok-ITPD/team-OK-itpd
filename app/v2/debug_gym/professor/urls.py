# [Professor Dev] URL routes for the professor app, mounted at /professor/
from django.urls import path

from .views import DashboardView

app_name = "professor"

urlpatterns = [path("", DashboardView.as_view(), name="dashboard")]
