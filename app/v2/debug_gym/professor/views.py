# [Professor Dev] Views for professor pages: groups, bugs, assignments, grading
from django.views.generic import TemplateView

from core.models import User
from core.permissions import RoleRequiredMixin


class DashboardView(RoleRequiredMixin, TemplateView):
    required_role = User.Role.PROFESSOR
    template_name = "professor/dashboard.html"
