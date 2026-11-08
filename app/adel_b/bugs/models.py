import hashlib
import secrets

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from accounts.models import Profile, role_of


class Bug(models.Model):
    """A prepared debugging exercise a learner can practise on."""

    PRIVATE = "private"
    PUBLIC = "public"
    GROUP = "group"
    AUDIENCES = [(PRIVATE, "Private"), (PUBLIC, "Public"), (GROUP, "Group")]

    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    language = models.CharField(max_length=50, default="Python 3")
    difficulty = models.CharField(max_length=20, default="Easy")
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
    audience = models.CharField(max_length=10, choices=AUDIENCES, default=PRIVATE)
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
        """Exercises the signed-in user may open, independent of list filters."""
        if not user.is_authenticated:
            return cls.objects.none()
        visible = (
            models.Q(created_by=user)
            | models.Q(audience=cls.PUBLIC)
            | models.Q(audience=cls.GROUP, assignments__group__memberships__student=user)
        )
        return cls.objects.filter(visible).distinct()

    @classmethod
    def filtered_for(cls, user, audience_filter):
        visible = cls.visible_to(user)
        if audience_filter == "my":
            return visible.filter(created_by=user)
        if audience_filter == "public":
            return visible.filter(audience=cls.PUBLIC)
        if audience_filter == "group":
            return visible.filter(
                audience=cls.GROUP, assignments__group__memberships__student=user
            ).distinct()
        if audience_filter == "all":
            return visible
        raise ValueError("Unknown audience filter.")

    def __str__(self) -> str:
        return self.title

    def clean(self):
        if (
            self.created_by_id
            and self.audience != self.PRIVATE
            and role_of(self.created_by) != Profile.PROFESSOR
        ):
            raise ValidationError({"audience": "Only a teacher can share or publish an exercise."})

    def to_dict(self) -> dict:
        return {
            "id": self.slug,
            "title": self.title,
            "language": self.language,
            "difficulty": self.difficulty,
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
            "audience": self.audience,
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


class TeachingGroup(models.Model):
    """A named student group owned by exactly one teacher."""

    name = models.CharField(max_length=150)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="teaching_groups"
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="GroupMembership", related_name="learning_groups"
    )

    class Meta:
        ordering = ["name", "id"]
        constraints = [
            models.UniqueConstraint(fields=["teacher", "name"], name="unique_group_name_per_teacher"),
        ]

    def __str__(self) -> str:
        return self.name

    def clean(self):
        if self.teacher_id and role_of(self.teacher) != Profile.PROFESSOR:
            raise ValidationError({"teacher": "Choose a professor account."})


class GroupMembership(models.Model):
    """Administrator-maintained membership of one student in a teaching group."""

    group = models.ForeignKey(TeachingGroup, on_delete=models.CASCADE, related_name="memberships")
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="group_memberships"
    )

    class Meta:
        ordering = ["student__username", "id"]
        constraints = [
            models.UniqueConstraint(fields=["group", "student"], name="one_membership_per_group_student"),
        ]

    def __str__(self) -> str:
        return f"{self.group}: {self.student}"

    def clean(self):
        if self.student_id and role_of(self.student) != Profile.STUDENT:
            raise ValidationError({"student": "Choose a student account."})


class Assignment(models.Model):
    """One exercise assigned to one teaching group on its own schedule."""

    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name="assignments")
    group = models.ForeignKey(TeachingGroup, on_delete=models.CASCADE, related_name="assignments")
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["deadline", "created_at"]
        constraints = [
            models.UniqueConstraint(fields=["bug", "group"], name="one_assignment_per_group_and_bug"),
        ]

    def __str__(self) -> str:
        return f"{self.bug} → {self.group}"

    def clean(self):
        if self.bug_id and self.group_id and self.bug.created_by_id != self.group.teacher_id:
            raise ValidationError("An exercise can only be assigned to its owner's group.")
