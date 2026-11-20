import uuid

from django.conf import settings
from django.db import models


class Profile(models.Model):
    """Extra account data: the user's role in Debug GYM."""

    STUDENT = "student"
    PROFESSOR = "professor"
    ROLES = [(STUDENT, "Student"), (PROFESSOR, "Professor")]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLES, default=STUDENT)
    # Random and unrelated to personal data: the only identifier analytics events carry.
    analytics_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def __str__(self) -> str:
        return f"{self.user.username} ({self.get_role_display()})"


def role_of(user) -> str:
    """The user's role; anyone without a profile yet counts as a student."""
    profile = getattr(user, "profile", None) if user.is_authenticated else None
    return profile.role if profile is not None else Profile.STUDENT


def is_professor(user) -> bool:
    return user.is_authenticated and role_of(user) == Profile.PROFESSOR
