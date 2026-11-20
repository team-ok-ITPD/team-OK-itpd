# [Student Dev] Tokens that let a student's VS Code submit a fix for one bug
import hashlib
import secrets

from django.conf import settings
from django.db import models

from core.models import Assignment, Bug


class IdeToken(models.Model):
    """Lets the VS Code extension submit for one student and one bug (and assignment).

    Only a hash of the key is stored; the key itself lives in the student's
    workspace folder. Opening VS Code again replaces the key.
    """

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ide_tokens")
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name="ide_tokens")
    # Null for practice.
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, null=True, blank=True, related_name="ide_tokens"
    )
    key_hash = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ide_tokens"

    def __str__(self):
        return f"VS Code token for {self.student} on {self.bug}"

    @staticmethod
    def hash(key):
        return hashlib.sha256(key.encode()).hexdigest()

    @classmethod
    def issue(cls, student, bug, assignment=None):
        """Create or replace the token for this student and work; return the new key."""
        key = secrets.token_urlsafe(32)
        cls.objects.update_or_create(
            student=student, bug=bug, assignment=assignment, defaults={"key_hash": cls.hash(key)}
        )
        return key

    @classmethod
    def find(cls, key):
        return cls.objects.select_related("student", "bug", "assignment").filter(key_hash=cls.hash(key)).first()
