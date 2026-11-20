# [Backend Dev] Tests for shared models
from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import Bug, Submission, User

PASSWORD = "debug-gym-pass"


class SubmissionTestCountsTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user("ali@example.com", "Ali", PASSWORD)
        prof = User.objects.create_user("sara@example.com", "Sara", PASSWORD, role=User.Role.PROFESSOR)
        self.bug = Bug.objects.create(
            title="Off by one", description="d", buggy_code="a", solution_code="b",
            language="python", difficulty=Bug.Difficulty.EASY,
            visibility=Bug.Visibility.PRIVATE, created_by=prof,
        )

    def make(self, passed, total):
        return Submission(
            student=self.student, bug=self.bug, submitted_code="x",
            tests_passed=passed, tests_total=total,
        )

    def test_counts_default_to_empty(self):
        submission = Submission.objects.create(student=self.student, bug=self.bug, submitted_code="x")
        self.assertIsNone(submission.tests_passed)
        self.assertIsNone(submission.test_result)

    def test_valid_counts_are_stored(self):
        submission = self.make(2, 3)
        submission.save()
        self.assertEqual(submission.test_result, "2/3")

    def test_passed_cannot_exceed_total(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            self.make(4, 3).save()

    def test_counts_are_both_set_or_both_empty(self):
        for passed, total in ((1, None), (None, 3)):
            with self.assertRaises(IntegrityError), transaction.atomic():
                self.make(passed, total).save()
