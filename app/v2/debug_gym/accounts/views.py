# [Backend Dev] Views for login, logout, register, profile and password reset
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import NoReverseMatch, reverse

from core.management.commands.seed_demo import DEFAULT_PASSWORD as DEMO_PASSWORD
from core.management.commands.seed_demo import email as demo_email
from core.models import User

from .forms import LoginForm

# Each role's home page, as "<app namespace>:dashboard".
ROLE_DASHBOARDS = {
    User.Role.ADMIN: "admin_panel:dashboard",
    User.Role.PROFESSOR: "professor:dashboard",
    User.Role.STUDENT: "student:dashboard",
}


# One demo account per role for the quick sign-in buttons (created by `manage.py seed_demo`).
DEMO_ACCOUNTS = [("admin", "Admin"), ("prof.karim", "Professor"), ("ali", "Student")]


def demo_logins():
    """Demo accounts to offer on the login page, or [] when DEMO_LOGIN is off."""
    if not settings.DEMO_LOGIN:
        return []
    emails = [demo_email(handle) for handle, _ in DEMO_ACCOUNTS]
    users = {u.email: u for u in User.objects.filter(email__in=emails, is_active=True)}
    return [
        {"label": label, "user": users[demo_email(handle)], "password": DEMO_PASSWORD}
        for handle, label in DEMO_ACCOUNTS
        if demo_email(handle) in users
    ]


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
        else:
            context["demo_logins"] = demo_logins()
        return context


class SignOutView(LogoutView):
    next_page = "accounts:login"
