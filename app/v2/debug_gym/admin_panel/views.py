# [Admin Dev] Views for admin pages: dashboard, users, groups, bugs, assignments, settings
from django.views.generic import TemplateView

from core.models import User
from core.permissions import RoleRequiredMixin


class DashboardView(RoleRequiredMixin, TemplateView):
    required_role = User.Role.ADMIN
    template_name = "admin_panel/dashboard.html"
