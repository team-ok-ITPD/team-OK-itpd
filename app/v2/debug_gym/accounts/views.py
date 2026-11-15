# [Backend Dev] Views for login, logout, register, profile and password reset
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import NoReverseMatch, reverse

from core.models import User

from .forms import LoginForm

# Each role's home page, as "<app namespace>:dashboard".
ROLE_DASHBOARDS = {
    User.Role.ADMIN: "admin_panel:dashboard",
    User.Role.PROFESSOR: "professor:dashboard",
    User.Role.STUDENT: "student:dashboard",
}


def role_home_url(user):
    """The user's dashboard, or the login page while that dashboard does not exist yet."""
    try:
        return reverse(ROLE_DASHBOARDS[user.role])
    except (KeyError, NoReverseMatch):
        return reverse("accounts:login")


class SignInView(LoginView):
    template_name = "accounts/login.html"
    form_class = LoginForm

    def get_default_redirect_url(self):
        # A safe ?next= link still wins; otherwise go to the role's dashboard.
        return role_home_url(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context["home_url"] = role_home_url(user)
            context["has_dashboard"] = context["home_url"] != reverse("accounts:login")
        return context


class SignOutView(LogoutView):
    next_page = "accounts:login"
