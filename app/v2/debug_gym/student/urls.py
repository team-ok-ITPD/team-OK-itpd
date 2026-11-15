# [Student Dev] URL routes for the student app, mounted at /student/
from django.urls import path

from .views import DashboardView

app_name = "student"

urlpatterns = [path("", DashboardView.as_view(), name="dashboard")]
