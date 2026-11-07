import datetime
import json

from django.contrib.auth import get_user_model
from django.db.models import ProtectedError
from django.test import Client, TestCase

from accounts.models import Profile

from .models import Assignment, Attempt, Bug, Draft

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
        Assignment.objects.create(bug=Bug.objects.get(slug=slug), student=self.alice, assigned_by=self.prof)
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

    def test_students_list_has_only_students(self):
        names = [student["username"] for student in self.client.get("/api/teach/students/").json()["students"]]
        self.assertEqual(names, ["alice", "bob"])

    def test_assign_with_due_date_and_see_progress(self):
        response = self.send("post", self.url, {"students": [self.alice.id, self.bob.id], "dueDate": "2026-12-01"})
        self.assertEqual(response.status_code, 200)
        bug = Bug.objects.get(slug=self.slug)
        Attempt.objects.create(user=self.alice, bug=bug, code="", passed_count=1, total_count=2)
        Attempt.objects.create(user=self.alice, bug=bug, code="", passed_count=2, total_count=2)
        Draft.objects.create(user=self.bob, bug=bug, code="x")
        rows = {row["username"]: row for row in self.client.get(self.url).json()["assignments"]}
        self.assertEqual((rows["alice"]["status"], rows["alice"]["bestPassed"], rows["alice"]["attempts"]), ("solved", 2, 2))
        self.assertEqual((rows["bob"]["status"], rows["bob"]["bestPassed"]), ("progress", None))
        self.assertEqual(rows["alice"]["dueDate"], "2026-12-01")

    def test_admin_accounts_are_not_students(self):
        admin = User.objects.create_superuser("boss", "boss@example.com", "debug-gym-pass")
        names = [student["username"] for student in self.client.get("/api/teach/students/").json()["students"]]
        self.assertNotIn("boss", names)
        self.assertEqual(self.send("post", self.url, {"students": [admin.id]}).status_code, 400)

    def test_reassigning_updates_the_due_date(self):
        self.send("post", self.url, {"students": [self.alice.id], "dueDate": "2026-12-01"})
        self.send("post", self.url, {"students": [self.alice.id], "dueDate": None})
        self.assertEqual(Assignment.objects.get().due_date, None)

    def test_only_students_can_be_assigned(self):
        response = self.send("post", self.url, {"students": [self.other_prof.id]})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.send("post", self.url, {"students": []}).status_code, 400)
        self.assertEqual(self.send("post", self.url, {"students": [self.alice.id], "dueDate": "soon"}).status_code, 400)
        self.assertFalse(Assignment.objects.exists())

    def test_unassign(self):
        self.send("post", self.url, {"students": [self.alice.id, self.bob.id]})
        response = self.client.delete(f"{self.url}{self.alice.id}/")
        self.assertEqual([row["username"] for row in response.json()["assignments"]], ["bob"])

    def test_other_professors_cannot_assign_or_see_results(self):
        self.as_user(self.other_prof)
        self.assertEqual(self.send("post", self.url, {"students": [self.alice.id]}).status_code, 404)
        self.assertEqual(self.client.get(self.url).status_code, 404)

    def test_students_cannot_use_professor_endpoints(self):
        self.as_user(self.alice)
        self.assertEqual(self.client.get("/api/teach/students/").status_code, 403)
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
        Assignment.objects.create(bug=Bug.objects.get(slug=self.slug), student=self.alice, assigned_by=self.prof)
        self.as_user(self.alice)
        self.assertIn(self.slug, self.bug_ids())
        response = self.send("post", f"/api/bugs/{self.slug}/attempts/", {"code": "x", "passed": 2, "total": 2})
        self.assertEqual(response.status_code, 201)
        self.as_user(self.bob)
        self.assertNotIn(self.slug, self.bug_ids())

    def test_professor_sees_own_exercise(self):
        self.as_user(self.prof)
        self.assertIn(self.slug, self.bug_ids())
        self.as_user(self.other_prof)
        self.assertNotIn(self.slug, self.bug_ids())

    def test_logged_out_sees_only_the_catalog(self):
        self.client.logout()
        self.assertEqual(len(self.bug_ids()), 5)


class MyAssignmentsTests(TeachingTestCase):
    def test_lists_my_assignments_with_status(self):
        slug = self.create()["id"]
        bug = Bug.objects.get(slug=slug)
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        Assignment.objects.create(bug=bug, student=self.alice, assigned_by=self.prof, due_date=yesterday)
        self.as_user(self.alice)
        item = self.client.get("/api/assignments/").json()["assignments"][0]
        self.assertEqual(
            (item["bugId"], item["assignedBy"], item["status"], item["overdue"]),
            (slug, "prof", "not-started", True),
        )
        Attempt.objects.create(user=self.alice, bug=bug, code="", passed_count=2, total_count=2)
        item = self.client.get("/api/assignments/").json()["assignments"][0]
        self.assertEqual((item["status"], item["overdue"]), ("solved", False))

    def test_others_assignments_are_not_listed(self):
        Assignment.objects.create(bug=Bug.objects.get(slug=self.create()["id"]), student=self.bob, assigned_by=self.prof)
        self.as_user(self.alice)
        self.assertEqual(self.client.get("/api/assignments/").json()["assignments"], [])

    def test_needs_login(self):
        self.assertEqual(Client().get("/api/assignments/").status_code, 401)


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
        Assignment.objects.create(bug=Bug.objects.get(slug=slug), student=self.alice, assigned_by=self.prof)
        self.alice.delete()
        self.assertFalse(Assignment.objects.exists())


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
        self.assertEqual(Assignment.objects.count(), 6)
        self.assertIn("| Professor | `prof_lina` |", text)
        password = text.split("| `prof_lina` | `prof_lina@debuggym.demo` | `")[1].split("`")[0]
        self.assertTrue(User.objects.get(username="prof_lina").check_password(password))
