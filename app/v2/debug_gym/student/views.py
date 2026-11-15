# [Student Dev] Views for student pages: assignments, bug workspace, practice, results
from django.views.generic import TemplateView

from core.models import User
from core.permissions import RoleRequiredMixin


class DashboardView(RoleRequiredMixin, TemplateView):
    required_role = User.Role.STUDENT
    template_name = "student/dashboard.html"
