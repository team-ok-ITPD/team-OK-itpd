import datetime
import json
from unittest import mock

from django.contrib.auth import get_user_model
from django.db.models import ProtectedError
from django.test import Client, TestCase

from accounts.models import Profile

from .models import Assignment, Attempt, Bug, Draft, GroupMembership, IdeToken, TeachingGroup

User = get_user_model()

EXERCISE = {
    "title": "The forgotten zero",
    "summary": "Counting zeros misses some.",
    "description": "count_zeros() should count every 0 in the list.",
    "difficulty": "Easy",
    "topic": "arrays",
    "functionName": "count_zeros",
    "buggyCode": "def count_zeros(numbers):\n    return numbers[1:].count(0)\n",
    "tests": [
        {"name": "No zeros", "input": "[1, 2]", "expected": "0"},
        {"name": "Leading zero", "input": "[0, 1, 0]", "expected": "2"},
    ],
}


def make(username, role=Profile.STUDENT):
    user = User.objects.create_user(username=username, email=f"{username}@example.com", password="debug-gym-pass")
    user.profile.role = role
    user.profile.save()
    return user


class TeachingTestCase(TestCase):
    def setUp(self):
        self.prof = make("prof", Profile.PROFESSOR)
        self.other_prof = make("other_prof", Profile.PROFESSOR)
        self.alice = make("alice")
        self.bob = make("bob")

    def as_user(self, user):
        self.client.force_login(user)

    def send(self, method, url, payload=None):
        return getattr(self.client, method)(url, data=json.dumps(payload or {}), content_type="application/json")

    def create(self, **changes):
        self.as_user(self.prof)
        response = self.send("post", "/api/teach/exercises/", {**EXERCISE, **changes})
        self.assertEqual(response.status_code, 201, response.content)
        return response.json()["exercise"]

    def group(self, name="Group A", teacher=None, students=()):
        group = TeachingGroup.objects.create(name=name, teacher=teacher or self.prof)
        GroupMembership.objects.bulk_create(
            [GroupMembership(group=group, student=student) for student in students]
        )
        return group


class ExerciseApiTests(TeachingTestCase):
    def test_professor_creates_an_exercise(self):
        exercise = self.create()
        bug = Bug.objects.get(slug=exercise["id"])
        self.assertEqual((bug.slug, bug.created_by, bug.file_name), ("the-forgotten-zero", self.prof, "count_zeros.py"))
        self.assertEqual(bug.tests[1], {"name": "Leading zero", "input": [0, 1, 0], "expected": 2})
        self.assertEqual(bug.topic, "Arrays & loops")
        self.assertEqual(exercise["editTests"][1], {"name": "Leading zero", "input": "[0, 1, 0]", "expected": "2"})

    def test_same_title_gets_a_new_slug(self):
        self.assertEqual(self.create()["id"], "the-forgotten-zero")
        self.assertEqual(self.create()["id"], "the-forgotten-zero-2")

    def test_students_cannot_create(self):
        self.as_user(self.alice)
        self.assertEqual(self.send("post", "/api/teach/exercises/", EXERCISE).status_code, 403)
        self.client.logout()
        self.assertEqual(self.send("post", "/api/teach/exercises/", EXERCISE).status_code, 401)

    def test_reports_every_invalid_field(self):
        self.as_user(self.prof)
        bad = {
            **EXERCISE,
            "title": "",
            "difficulty": "Impossible",
            "functionName": "count zeros",
            "tests": [{"name": "", "input": "[1,", "expected": "__import__('os')"}],
        }
        response = self.send("post", "/api/teach/exercises/", bad)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            set(response.json()["fields"]),
            {"title", "difficulty", "functionName", "tests.0.name", "tests.0.input", "tests.0.expected"},
        )

    def test_code_must_define_the_function(self):
        self.as_user(self.prof)
        response = self.send("post", "/api/teach/exercises/", {**EXERCISE, "buggyCode": "def other():\n    pass\n"})
        self.assertIn("buggyCode", response.json()["fields"])

    def test_needs_at_least_one_test(self):
        self.as_user(self.prof)
        response = self.send("post", "/api/teach/exercises/", {**EXERCISE, "tests": []})
        self.assertIn("tests", response.json()["fields"])

    def test_list_shows_only_own_exercises_with_counts(self):
        slug = self.create()["id"]
        group = self.group(students=[self.alice])
        Assignment.objects.create(bug=Bug.objects.get(slug=slug), group=group)
        Attempt.objects.create(user=self.alice, bug=Bug.objects.get(slug=slug), code="", passed_count=2, total_count=2)
        items = self.client.get("/api/teach/exercises/").json()["exercises"]
        self.assertEqual([(item["id"], item["assigned"], item["solved"]) for item in items], [(slug, 1, 1)])
        self.as_user(self.other_prof)
        self.assertEqual(self.client.get("/api/teach/exercises/").json()["exercises"], [])

    def test_owner_edits_and_others_cannot(self):
        slug = self.create()["id"]
        response = self.send("put", f"/api/teach/exercises/{slug}/", {**EXERCISE, "title": "Renamed"})
        self.assertEqual(response.json()["exercise"]["title"], "Renamed")
        self.assertEqual(Bug.objects.get(slug=slug).title, "Renamed")
        self.as_user(self.other_prof)
        self.assertEqual(self.send("put", f"/api/teach/exercises/{slug}/", EXERCISE).status_code, 404)
        self.assertEqual(self.client.delete(f"/api/teach/exercises/{slug}/").status_code, 404)

    def test_changing_tests_resets_learners_edited_copies(self):
        slug = self.create()["id"]
        bug = Bug.objects.get(slug=slug)
        Draft.objects.create(user=self.alice, bug=bug, code="x", tests=[{"name": "mine", "input": [], "expected": 0}])
        new_tests = EXERCISE["tests"] + [{"name": "All zeros", "input": "[0, 0]", "expected": "2"}]
        self.send("put", f"/api/teach/exercises/{slug}/", {**EXERCISE, "tests": new_tests})
        self.assertIsNone(Draft.objects.get(user=self.alice, bug=bug).tests)

    def test_owner_deletes(self):
        slug = self.create()["id"]
        self.assertEqual(self.client.delete(f"/api/teach/exercises/{slug}/").status_code, 200)
        self.assertFalse(Bug.objects.filter(slug=slug).exists())

    def test_catalog_bugs_cannot_be_edited(self):
        self.as_user(self.prof)
        self.assertEqual(self.client.get("/api/teach/exercises/remove-negatives/").status_code, 404)


class AssignmentApiTests(TeachingTestCase):
    def setUp(self):
        super().setUp()
        self.slug = self.create()["id"]
        self.url = f"/api/teach/exercises/{self.slug}/assignments/"
        self.group_a = self.group("Group A", students=[self.alice, self.bob])
        self.group_b = self.group("Group B", students=[self.bob])

    def test_groups_list_has_only_the_teachers_groups(self):
        self.group("Other", teacher=self.other_prof, students=[self.alice])
        groups = self.client.get("/api/teach/groups/").json()["groups"]
        self.assertEqual([(group["name"], group["memberCount"]) for group in groups], [("Group A", 2), ("Group B", 1)])

    def test_assign_group_with_deadline_and_see_member_progress(self):
        response = self.send("post", self.url, {"groups": [self.group_a.id], "deadline": "2026-12-01"})
        self.assertEqual(response.status_code, 200)
        bug = Bug.objects.get(slug=self.slug)
        Attempt.objects.create(user=self.alice, bug=bug, code="", passed_count=1, total_count=2)
        Attempt.objects.create(user=self.alice, bug=bug, code="", passed_count=2, total_count=2)
        Draft.objects.create(user=self.bob, bug=bug, code="x")
        assignment = self.client.get(self.url).json()["assignments"][0]
        rows = {row["username"]: row for row in assignment["members"]}
        self.assertEqual((rows["alice"]["status"], rows["alice"]["bestPassed"], rows["alice"]["attempts"]), ("solved", 2, 2))
        self.assertEqual((rows["bob"]["status"], rows["bob"]["bestPassed"]), ("progress", None))
        self.assertEqual((assignment["groupName"], assignment["deadline"]), ("Group A", "2026-12-01"))

    def test_other_teachers_group_cannot_be_assigned(self):
        other = self.group("Other", teacher=self.other_prof, students=[self.alice])
        self.assertEqual(self.send("post", self.url, {"groups": [other.id]}).status_code, 400)

    def test_each_group_has_an_independent_deadline(self):
        self.send("post", self.url, {"groups": [self.group_a.id], "deadline": "2026-12-01"})
        self.send("post", self.url, {"groups": [self.group_b.id], "deadline": "2026-12-10"})
        deadlines = {row.group.name: row.deadline.isoformat() for row in Assignment.objects.all()}
        self.assertEqual(deadlines, {"Group A": "2026-12-01", "Group B": "2026-12-10"})

    def test_assignment_input_is_validated(self):
        self.assertEqual(self.send("post", self.url, {"groups": []}).status_code, 400)
        self.assertEqual(self.send("post", self.url, {"groups": [self.group_a.id], "deadline": "soon"}).status_code, 400)
        self.assertFalse(Assignment.objects.exists())

    def test_unassign(self):
        response = self.send("post", self.url, {"groups": [self.group_a.id, self.group_b.id]})
        assignment_id = response.json()["assignments"][0]["assignmentId"]
        response = self.client.delete(f"{self.url}{assignment_id}/")
        self.assertEqual(len(response.json()["assignments"]), 1)

    def test_other_professors_cannot_assign_or_see_results(self):
        self.as_user(self.other_prof)
        self.assertEqual(self.send("post", self.url, {"groups": [self.group_a.id]}).status_code, 404)
        self.assertEqual(self.client.get(self.url).status_code, 404)

    def test_students_cannot_use_professor_endpoints(self):
        self.as_user(self.alice)
        self.assertEqual(self.client.get("/api/teach/groups/").status_code, 403)
        self.assertEqual(self.client.get(self.url).status_code, 403)


class StudentVisibilityTests(TeachingTestCase):
    def setUp(self):
        super().setUp()
        self.slug = self.create()["id"]

    def bug_ids(self):
        return [bug["id"] for bug in self.client.get("/api/bugs/").json()["bugs"]]

    def test_unassigned_professor_exercise_is_hidden(self):
        self.as_user(self.alice)
        self.assertNotIn(self.slug, self.bug_ids())
        self.assertIn("remove-negatives", self.bug_ids())
        for url in (
            f"/api/bugs/{self.slug}/",
            f"/api/bugs/{self.slug}/draft/",
            f"/api/bugs/{self.slug}/attempts/",
        ):
            self.assertEqual(self.client.get(url).status_code, 404, url)
        self.assertEqual(self.send("post", f"/api/bugs/{self.slug}/vscode/").status_code, 404)

    def test_search_does_not_find_hidden_exercises(self):
        self.as_user(self.alice)
        response = self.send("post", "/api/exercises", {"query": "forgotten zero"})
        self.assertNotIn(self.slug, [bug["id"] for bug in response.json().get("exercises", [])])

    def test_assigned_student_sees_and_submits(self):
        group = self.group(students=[self.alice])
        Assignment.objects.create(bug=Bug.objects.get(slug=self.slug), group=group)
        self.as_user(self.alice)
        self.assertIn(self.slug, self.bug_ids())
        with mock.patch("bugs.verification.verify_submission", return_value=(2, 2)):
            response = self.send("post", f"/api/bugs/{self.slug}/attempts/", {"code": "x", "passed": 2, "total": 2})
        self.assertEqual(response.status_code, 201)
        self.as_user(self.bob)
        self.assertNotIn(self.slug, self.bug_ids())

    def test_professor_sees_own_exercise(self):
        self.as_user(self.prof)
        self.assertIn(self.slug, self.bug_ids())
        self.as_user(self.other_prof)
        self.assertNotIn(self.slug, self.bug_ids())

    def test_membership_removal_revokes_access_without_deleting_work(self):
        bug = Bug.objects.get(slug=self.slug)
        group = self.group(students=[self.alice])
        Assignment.objects.create(bug=bug, group=group)
        Attempt.objects.create(user=self.alice, bug=bug, code="work", passed_count=1, total_count=2)
        GroupMembership.objects.get(group=group, student=self.alice).delete()
        self.as_user(self.alice)
        self.assertNotIn(self.slug, self.bug_ids())
        self.assertTrue(Attempt.objects.filter(user=self.alice, bug=bug).exists())

    def test_membership_removal_revokes_an_existing_ide_token(self):
        bug = Bug.objects.get(slug=self.slug)
        group = self.group(students=[self.alice])
        Assignment.objects.create(bug=bug, group=group)
        key = IdeToken.issue(self.alice, bug)
        GroupMembership.objects.get(group=group, student=self.alice).delete()
        with mock.patch("bugs.verification.verify_submission") as verify:
            response = self.send_with_token(key, {
                "bug": bug.slug,
                "code": "def count_zeros(numbers): return 0",
            })
        self.assertEqual(response.status_code, 403)
        self.assertFalse(IdeToken.objects.filter(user=self.alice, bug=bug).exists())
        verify.assert_not_called()

    def send_with_token(self, key, payload):
        return Client(enforce_csrf_checks=True).post(
            "/api/ide/submit/",
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {key}",
        )

    def test_logged_out_sees_only_the_catalog(self):
        self.client.logout()
        self.assertEqual(len(self.bug_ids()), 5)


class MyAssignmentsTests(TeachingTestCase):
    def test_lists_my_assignments_with_status(self):
        slug = self.create()["id"]
        bug = Bug.objects.get(slug=slug)
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        group = self.group(students=[self.alice])
        Assignment.objects.create(bug=bug, group=group, deadline=yesterday)
        self.as_user(self.alice)
        item = self.client.get("/api/assignments/").json()["assignments"][0]
        self.assertEqual(
            (item["bugId"], item["groupName"], item["assignedBy"], item["status"], item["overdue"]),
            (slug, "Group A", "prof", "not-started", True),
        )
        Attempt.objects.create(user=self.alice, bug=bug, code="", passed_count=2, total_count=2)
        item = self.client.get("/api/assignments/").json()["assignments"][0]
        self.assertEqual((item["status"], item["overdue"]), ("solved", False))

    def test_others_assignments_are_not_listed(self):
        group = self.group(students=[self.bob])
        Assignment.objects.create(bug=Bug.objects.get(slug=self.create()["id"]), group=group)
        self.as_user(self.alice)
        self.assertEqual(self.client.get("/api/assignments/").json()["assignments"], [])

    def test_needs_login(self):
        self.assertEqual(Client().get("/api/assignments/").status_code, 401)

    def test_same_exercise_keeps_each_group_deadline(self):
        bug = Bug.objects.get(slug=self.create()["id"])
        first = self.group("First", students=[self.alice])
        second = self.group("Second", students=[self.alice])
        Assignment.objects.create(bug=bug, group=first, deadline="2026-12-01")
        Assignment.objects.create(bug=bug, group=second, deadline="2026-12-10")
        self.as_user(self.alice)
        rows = self.client.get("/api/assignments/").json()["assignments"]
        self.assertEqual([(row["groupName"], row["deadline"]) for row in rows], [
            ("First", "2026-12-01"),
            ("Second", "2026-12-10"),
        ])


class GroupAdminTests(TeachingTestCase):
    def test_admin_creates_a_group_and_maintains_membership(self):
        admin = User.objects.create_superuser("boss", "boss@example.com", "debug-gym-pass")
        self.client.force_login(admin)
        response = self.client.post(
            "/admin/bugs/teachinggroup/add/",
            {
                "name": "CS-101",
                "teacher": self.prof.id,
                "memberships-TOTAL_FORMS": "1",
                "memberships-INITIAL_FORMS": "0",
                "memberships-MIN_NUM_FORMS": "0",
                "memberships-MAX_NUM_FORMS": "1000",
                "memberships-0-student": self.alice.id,
                "_save": "Save",
            },
        )
        self.assertEqual(response.status_code, 302, response.context and response.context.get("adminform"))
        group = TeachingGroup.objects.get(name="CS-101")
        self.assertEqual((group.teacher, list(group.students.all())), (self.prof, [self.alice]))

    def test_teacher_cannot_open_group_admin(self):
        self.as_user(self.prof)
        response = self.client.get("/admin/bugs/teachinggroup/add/")
        self.assertEqual(response.status_code, 302)

    def test_staff_professor_cannot_manage_membership(self):
        self.prof.is_staff = True
        self.prof.save(update_fields=["is_staff"])
        self.as_user(self.prof)
        self.assertNotEqual(self.client.get("/admin/bugs/teachinggroup/add/").status_code, 200)

    def test_group_roles_and_assignment_ownership_are_validated(self):
        from django.core.exceptions import ValidationError

        with self.assertRaises(ValidationError):
            TeachingGroup(name="Invalid", teacher=self.alice).full_clean()
        group = self.group(teacher=self.other_prof, students=[self.alice])
        with self.assertRaises(ValidationError):
            GroupMembership(group=group, student=self.prof).full_clean()
        bug = Bug.objects.get(slug=self.create()["id"])
        with self.assertRaises(ValidationError):
            Assignment(bug=bug, group=group).full_clean()


class DeletingProfessorsTests(TeachingTestCase):
    def test_professor_with_exercises_cannot_be_deleted(self):
        slug = self.create()["id"]
        with self.assertRaises(ProtectedError):
            self.prof.delete()
        self.assertEqual(Bug.objects.get(slug=slug).created_by, self.prof)

    def test_admin_shows_why_it_cannot_delete(self):
        self.create()
        admin = User.objects.create_superuser("boss", "boss@example.com", "debug-gym-pass")
        self.client.force_login(admin)
        response = self.client.post(f"/admin/auth/user/{self.prof.id}/delete/", {"post": "yes"})
        self.assertContains(response, "The forgotten zero")
        self.assertTrue(User.objects.filter(id=self.prof.id).exists())

    def test_professor_can_be_deleted_once_exercises_are_gone(self):
        slug = self.create()["id"]
        self.client.delete(f"/api/teach/exercises/{slug}/")
        self.prof.delete()
        self.assertFalse(User.objects.filter(username="prof").exists())

    def test_students_are_still_deleted_normally(self):
        slug = self.create()["id"]
        group = self.group(students=[self.alice])
        Assignment.objects.create(bug=Bug.objects.get(slug=slug), group=group)
        self.alice.delete()
        self.assertTrue(Assignment.objects.exists())
        self.assertFalse(GroupMembership.objects.exists())


class SeedDemoTests(TestCase):
    def test_creates_accounts_progress_and_file_and_can_rerun(self):
        import tempfile
        from pathlib import Path

        from django.core.management import call_command

        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "accounts.md"
            call_command("seed_demo", output=str(output), stdout=open("/dev/null", "w"))
            call_command("seed_demo", output=str(output), stdout=open("/dev/null", "w"))
            text = output.read_text()
        self.assertEqual(User.objects.filter(username__in=["prof_lina", "student_ali", "student_maria", "student_omar", "demo_admin"]).count(), 5)
        self.assertEqual(User.objects.get(username="prof_lina").profile.role, Profile.PROFESSOR)
        self.assertEqual(Bug.objects.filter(created_by__username="prof_lina").count(), 2)
        self.assertEqual(Assignment.objects.count(), 2)
        self.assertEqual(TeachingGroup.objects.get(name="Debug GYM 2026").memberships.count(), 3)
        self.assertIn("| Professor | `prof_lina` |", text)
        password = text.split("| `prof_lina` | `prof_lina@debuggym.demo` | `")[1].split("`")[0]
        self.assertTrue(User.objects.get(username="prof_lina").check_password(password))
