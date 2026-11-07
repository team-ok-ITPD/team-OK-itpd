import hashlib
import secrets

from django.conf import settings
from django.db import models


class Bug(models.Model):
    """A prepared debugging exercise a learner can practise on."""

    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    language = models.CharField(max_length=50, default="Python 3")
    difficulty = models.CharField(max_length=20, default="Easy")
    duration = models.CharField(max_length=30, blank=True)
    category = models.SlugField(default="arrays")
    topic = models.CharField(max_length=100, blank=True)
    summary = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    file_name = models.CharField(max_length=100, blank=True)
    function_name = models.CharField(max_length=100, blank=True)
    buggy_code = models.TextField(blank=True)
    tests = models.JSONField(default=list, blank=True)
    symptom = models.CharField(max_length=200, blank=True)
    explanation = models.TextField(blank=True)
    has_workspace = models.BooleanField(default=False)
    # The professor who wrote it; empty for the built-in catalog every learner can open.
    # PROTECT: deleting the professor must not turn their private exercises into catalog ones.
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="created_bugs",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    @classmethod
    def visible_to(cls, user):
        """The catalog, plus a professor's own exercises or a student's assigned ones."""
        visible = models.Q(created_by__isnull=True)
        if user.is_authenticated:
            visible |= models.Q(created_by=user) | models.Q(assignments__student=user)
        return cls.objects.filter(visible).distinct()

    def __str__(self) -> str:
        return self.title

    def to_dict(self) -> dict:
        return {
            "id": self.slug,
            "title": self.title,
            "language": self.language,
            "difficulty": self.difficulty,
            "duration": self.duration,
            "topic": self.category,
            "topicLabel": self.topic,
            "summary": self.summary,
            "description": self.description,
            "file": self.file_name,
            "functionName": self.function_name,
            "buggyCode": self.buggy_code,
            "tests": self.tests,
            "symptom": self.symptom,
            "explanation": self.explanation,
            "workspace": self.has_workspace,
            "workspaceUrl": settings.DEBUG_GYM_WORKSPACE_URL if self.has_workspace else None,
            "createdBy": self.created_by.username if self.created_by else None,
        }


class Draft(models.Model):
    """The learner's edited version of a bug's code."""

    # Rows saved before accounts existed have no user and are no longer shown.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="drafts"
    )
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name="drafts")
    code = models.TextField()
    # The learner's own copy of the bug's tests once they edit one; None means unchanged.
    tests = models.JSONField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "bug"], name="one_draft_per_user_and_bug"),
        ]

    def to_dict(self) -> dict:
        return {
            "bugId": self.bug.slug,
            "code": self.code,
            "tests": self.tests,
            "updatedAt": self.updated_at.isoformat(),
        }


class Attempt(models.Model):
    """One submitted solution and how many of the bug's tests it passed."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="attempts"
    )
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name="attempts")
    code = models.TextField()
    passed_count = models.PositiveIntegerField()
    total_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    @property
    def solved(self) -> bool:
        return self.total_count > 0 and self.passed_count == self.total_count

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "bugId": self.bug.slug,
            "passed": self.passed_count,
            "total": self.total_count,
            "solved": self.solved,
            "createdAt": self.created_at.isoformat(),
        }


class IdeToken(models.Model):
    """Lets the VS Code extension submit for one user and bug; only a hash is stored."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ide_tokens")
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name="ide_tokens")
    key_hash = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "bug"], name="one_ide_token_per_user_and_bug"),
        ]

    @staticmethod
    def hash(key: str) -> str:
        return hashlib.sha256(key.encode()).hexdigest()

    @classmethod
    def issue(cls, user, bug) -> str:
        """Create or replace the user's token for this bug and return the new key."""
        key = secrets.token_urlsafe(32)
        cls.objects.update_or_create(user=user, bug=bug, defaults={"key_hash": cls.hash(key)})
        return key

    @classmethod
    def find(cls, key: str):
        return cls.objects.select_related("user", "bug").filter(key_hash=cls.hash(key)).first()


class Assignment(models.Model):
    """A professor's exercise given to one student, with an optional due date."""

    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name="assignments")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assignments")
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="assigned"
    )
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["due_date", "created_at"]
        constraints = [
            models.UniqueConstraint(fields=["bug", "student"], name="one_assignment_per_student_and_bug"),
        ]

    def __str__(self) -> str:
        return f"{self.bug} → {self.student}"
