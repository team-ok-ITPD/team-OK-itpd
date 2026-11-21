# [Backend Dev] Tests for shared models and the demo seed command
from io import StringIO

from django.core.management import CommandError, call_command
from django.db import IntegrityError, transaction
from django.test import TestCase

from student.views import attach_status, my_assignments

from .models import Assignment, Bug, StudyGroup, Submission, User

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


def seed(*args):
    out = StringIO()
    call_command("seed_demo", *args, "--password", "test-pass", stdout=out)
    return out.getvalue()


class SeedDemoTests(TestCase):
    def test_creates_every_kind_of_example(self):
        output = seed()
        self.assertIn("Demo data added.", output)
        self.assertIn("ali@demo.debuggym.test", output)
        self.assertEqual(User.objects.filter(role=User.Role.ADMIN).count(), 1)
        self.assertEqual(User.objects.filter(role=User.Role.PROFESSOR).count(), 2)
        self.assertEqual(User.objects.filter(role=User.Role.STUDENT).count(), 8)
        self.assertEqual(StudyGroup.objects.count(), 3)
        self.assertTrue(Bug.objects.filter(visibility=Bug.Visibility.PUBLIC).exists())
        self.assertTrue(Bug.objects.filter(created_by__role=User.Role.STUDENT).exists())
        self.assertTrue(Submission.objects.filter(status=Submission.Status.GRADED).exists())
        self.assertTrue(Submission.objects.filter(assignment__isnull=True).exists())
        self.assertTrue(User.objects.get(email="ali@demo.debuggym.test").check_password("test-pass"))

    def test_ali_sees_every_status(self):
        seed()
        ali = User.objects.get(email="ali@demo.debuggym.test")
        statuses = {a.my_status for a in attach_status(my_assignments(ali), ali)}
        self.assertEqual(statuses, {"todo", "submitted", "graded", "missed"})

    def test_running_twice_needs_reset(self):
        seed()
        with self.assertRaises(CommandError):
            seed()
        seed("--reset")
        self.assertEqual(User.objects.filter(email__endswith="@demo.debuggym.test").count(), 11)

    def test_delete_only_touches_demo_data(self):
        real_prof = User.objects.create_user("real@school.edu", "Real Prof", "x", role=User.Role.PROFESSOR)
        real_bug = Bug.objects.create(
            title="Real bug", description="d", buggy_code="x", solution_code="y", language="python",
            difficulty="easy", visibility="public", created_by=real_prof,
        )
        seed()
        seed("--delete")
        self.assertFalse(User.objects.filter(email__endswith="@demo.debuggym.test").exists())
        self.assertFalse(Assignment.objects.exists())
        self.assertTrue(User.objects.filter(pk=real_prof.pk).exists())
        self.assertTrue(Bug.objects.filter(pk=real_bug.pk).exists())
