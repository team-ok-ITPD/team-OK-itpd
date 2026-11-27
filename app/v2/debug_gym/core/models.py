# [Backend Dev] Shared models: User, StudyGroup, Bug, Assignment, Submission
import hashlib
import secrets
from datetime import timedelta

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models import F, Q
from django.db.models.functions import Lower
from django.utils import timezone


class UserManager(BaseUserManager):
    """Creates users identified by email instead of username."""

    use_in_migrations = True

    def create_user(self, email, name, password=None, role="student", **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email), name=name, role=role, **extra_fields
        )
        user.set_password(password)  # stores a hash, never the raw password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        return self.create_user(email, name, password, role=User.Role.ADMIN, **extra_fields)

    def get_by_natural_key(self, email):
        # Log in with any letter case: ALI@example.com finds ali@example.com.
        return self.get(email__iexact=email)


class User(AbstractBaseUser):
    """Table 1: users."""

    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        PROFESSOR = "professor", "Professor"
        STUDENT = "student", "Student"

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    # password (hashed, VARCHAR) is provided by AbstractBaseUser
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    avatar_url = models.URLField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        db_table = "users"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} <{self.email}>"

    # Role helpers
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_professor(self):
        return self.role == self.Role.PROFESSOR

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    # Django admin access is derived from the role instead of extra columns
    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_active and self.is_admin

    def has_module_perms(self, app_label):
        return self.is_active and self.is_admin


class StudyGroup(models.Model):
    """Table 2: groups. One professor -> many groups."""

    name = models.CharField(max_length=100)
    course = models.CharField(max_length=200, blank=True)
    group_number = models.CharField(max_length=50, blank=True, default="")
    description = models.TextField(null=True, blank=True)
    professor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="taught_groups",
        limit_choices_to={"role": User.Role.PROFESSOR},
    )
    students = models.ManyToManyField(
        User,
        through="GroupStudent",
        related_name="study_groups",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "groups"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                Lower("name"), Lower("group_number"),
                condition=~Q(group_number=""),
                name="unique_course_group_number",
            ),
        ]

    def __str__(self):
        return f"{self.name} · {self.group_number}" if self.group_number else self.name


class GroupStudent(models.Model):
    """Table 3: group_students. Student <-> Group (N:N)."""

    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role": User.Role.STUDENT},
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "group_students"
        constraints = [
            models.UniqueConstraint(fields=["group", "student"], name="unique_group_student"),
        ]

    def __str__(self):
        return f"{self.student} in {self.group}"


class Bug(models.Model):
    """Table 4: bugs."""

    class Difficulty(models.TextChoices):
        EASY = "easy", "Easy"
        MEDIUM = "medium", "Medium"
        HARD = "hard", "Hard"

    class Visibility(models.TextChoices):
        PUBLIC = "public", "Public"
        PRIVATE = "private", "Private"

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    buggy_code = models.TextField(help_text="Code with the bug")
    language = models.CharField(max_length=50, help_text="e.g. python, dart")
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices, blank=True, default=Difficulty.EASY)
    visibility = models.CharField(max_length=10, choices=Visibility.choices)
    project_files = models.JSONField(default=dict, blank=True)
    compose_config = models.TextField(blank=True)
    dockerfile_config = models.TextField(blank=True)
    # Older single-file test field, still used by the professor pages. Tests also live
    # in project_files (test_main.py), which VS Code and server verification read.
    tests_code = models.TextField(
        blank=True,
        default="",
        help_text="Optional pytest file for Python bugs. The code is saved as main.py, "
        "so tests start with: from main import *",
    )
    entry_file = models.CharField(max_length=255, blank=True)
    revision = models.PositiveIntegerField(default=1)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_bugs",
        db_column="created_by",
        limit_choices_to={"role__in": [User.Role.ADMIN, User.Role.PROFESSOR]},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "bugs"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Assignment(models.Model):
    """Table 5: assignments. Assignment -> Bug (N:1)."""

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        CLOSED = "closed", "Closed"

    title = models.CharField(max_length=200)
    instructions = models.TextField(null=True, blank=True)
    bug = models.ForeignKey(Bug, on_delete=models.PROTECT, related_name="assignments")
    professor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_assignments",
        limit_choices_to={"role__in": [User.Role.ADMIN, User.Role.PROFESSOR]},
    )
    groups = models.ManyToManyField(
        StudyGroup,
        through="AssignmentGroup",
        related_name="assignments",
        blank=True,
    )
    deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    is_withdrawn = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "assignments"
        ordering = ["deadline"]

    def __str__(self):
        return self.title

    @property
    def results_visible(self):
        from django.utils import timezone

        return self.status == self.Status.CLOSED or (
            self.deadline is not None and self.deadline <= timezone.now()
        )


class AssignmentGroup(models.Model):
    """Table 6: assignment_groups. Assignment <-> Group (N:N)."""

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "assignment_groups"
        constraints = [
            models.UniqueConstraint(fields=["assignment", "group"], name="unique_assignment_group"),
        ]

    def __str__(self):
        return f"{self.assignment} -> {self.group}"


class Submission(models.Model):
    """Table 7: submissions. assignment is null for practice attempts."""

    class Status(models.TextChoices):
        SUBMITTED = "submitted", "Submitted"
        GRADED = "graded", "Graded"

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="submissions",
        limit_choices_to={"role": User.Role.STUDENT},
    )
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name="submissions")
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions",
        null=True,
        blank=True,
    )
    submitted_code = models.TextField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.SUBMITTED)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    # Test results come from server-side verification only (DEC-037); null means
    # "not verified yet". They are never read from a form or the browser.
    tests_passed = models.PositiveIntegerField(null=True, blank=True)
    tests_total = models.PositiveIntegerField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    graded_at = models.DateTimeField(null=True, blank=True)
    suspicion_status = models.CharField(max_length=16, default="unchecked")
    suspicion_reason = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "submissions"
        ordering = ["-submitted_at"]
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(tests_passed__isnull=True, tests_total__isnull=True)
                    | models.Q(
                        tests_passed__isnull=False,
                        tests_total__isnull=False,
                        tests_passed__lte=models.F("tests_total"),
                    )
                ),
                name="submission_valid_test_counts",
            ),
        ]

    def __str__(self):
        return f"{self.student} - {self.bug} ({self.status})"

    @property
    def is_practice(self):
        return self.assignment_id is None

    @property
    def test_result(self):
        """"3/5" when test counts are recorded, otherwise None."""
        if self.tests_passed is None or self.tests_total is None:
            return None
        return f"{self.tests_passed}/{self.tests_total}"


class AgentCredential(models.Model):
    class Provider(models.TextChoices):
        PLATFORM = "platform", "Platform provider"
        OPENAI = "openai", "OpenAI"
        OPENROUTER = "openrouter", "OpenRouter"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="agent_credential")
    encrypted_key = models.TextField(blank=True)
    provider = models.CharField(max_length=20, choices=Provider.choices, default=Provider.PLATFORM)
    # Students' AI bug generator: their own OpenAI-compatible endpoint and model.
    endpoint = models.URLField(max_length=500, blank=True)
    model = models.CharField(max_length=100, blank=True)


class WorkspaceSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, null=True, blank=True, on_delete=models.CASCADE)
    authoring = models.BooleanField(default=False)
    token_digest = models.CharField(max_length=64, unique=True)
    revision = models.PositiveIntegerField()
    expires_at = models.DateTimeField()
    last_request = models.CharField(max_length=64, blank=True)
    last_response = models.JSONField(default=dict, blank=True)


class WorkspacePairingCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workspace_pairing_codes")
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, null=True, blank=True, on_delete=models.CASCADE)
    code_digest = models.CharField(max_length=64, unique=True)
    site_url = models.URLField(max_length=500)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def digest(code):
        return hashlib.sha256(code.encode("ascii")).hexdigest()

    @classmethod
    def issue(cls, user, bug, assignment, site_url):
        code = secrets.token_hex(12).upper()
        cls.objects.create(
            user=user,
            bug=bug,
            assignment=assignment,
            code_digest=cls.digest(code),
            site_url=site_url,
            expires_at=timezone.now() + timedelta(minutes=10),
        )
        return code


class AssignmentReview(models.Model):
    assignment = models.OneToOneField(Assignment, on_delete=models.CASCADE, related_name="agent_review")
    status = models.CharField(max_length=16, default="running")
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    detail = models.TextField(blank=True)
