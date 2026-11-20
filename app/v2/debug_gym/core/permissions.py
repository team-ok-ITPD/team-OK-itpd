# [Backend Dev] Role decorators and mixins for admin, professor and student access
from functools import wraps

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied

from .models import User


def role_required(*roles):
    """Allow only signed-in users whose role is one of `roles`.

    Signed-out visitors go to the login page (and come back after signing in);
    a signed-in user with another role gets 403 Forbidden.
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if request.user.role not in roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


admin_required = role_required(User.Role.ADMIN)
professor_required = role_required(User.Role.PROFESSOR)
student_required = role_required(User.Role.STUDENT)


class RoleRequiredMixin(LoginRequiredMixin):
    """Class-based view version.

    Set `required_role = User.Role.ADMIN` for one role, or
    `allowed_roles = [User.Role.ADMIN, User.Role.PROFESSOR]` for several.
    A view that sets neither denies everyone.
    """

    allowed_roles = ()
    required_role = None

    def get_allowed_roles(self):
        if self.allowed_roles:
            return tuple(self.allowed_roles)
        if self.required_role:
            return (self.required_role,)
        return ()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role not in self.get_allowed_roles():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
