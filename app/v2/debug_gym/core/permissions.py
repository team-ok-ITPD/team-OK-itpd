# [Backend Dev] Role decorators and mixins for admin, professor and student access
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Allow one explicitly named product role and deny every other role."""

    required_role = None

    def test_func(self):
        return (
            self.request.user.is_active
            and self.request.user.role == self.required_role
        )

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied
        return super().handle_no_permission()
