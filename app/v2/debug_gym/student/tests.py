# [Student Dev] Tests for the student pages
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.models import Assignment, Bug, StudyGroup, Submission, User

PASSWORD = "debug-gym-pass"


class StudentTestCase(TestCase):
    """Shared data: Ali and Omar in Group A, Sara as their professor, one private bug."""

    url = reverse("student:dashboard")

    def setUp(self):
        self.student = User.objects.create_user("ali@example.com", "Ali", PASSWORD)
        self.other = User.objects.create_user("omar@example.com", "Omar", PASSWORD)
        self.prof = User.objects.create_user(
            "sara@example.com", "Sara", PASSWORD, role=User.Role.PROFESSOR
        )
        self.group = StudyGroup.objects.create(name="Group A", professor=self.prof)
        self.group.students.add(self.student, self.other)
        self.other_group = StudyGroup.objects.create(name="Group B", professor=self.prof)
        self.bug = Bug.objects.create(
            title="Off by one",
            description="Loop skips the last item",
            buggy_code="for i in range(len(x) - 1): pass",
            solution_code="for i in range(len(x)): pass",
            language="python",
            difficulty=Bug.Difficulty.EASY,
            visibility=Bug.Visibility.PRIVATE,
            created_by=self.prof,
        )

    def assignment(self, title, group=None, days=3, **extra):
        a = Assignment.objects.create(
            title=title,
            bug=self.bug,
            professor=self.prof,
            deadline=timezone.now() + timedelta(days=days),
            **extra,
        )
        a.groups.add(group or self.group)
        return a

    def get(self, user=None):
        self.client.force_login(user or self.student)
        return self.client.get(self.url)


class DashboardTests(StudentTestCase):
    def test_signed_out_visitor_goes_to_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={self.url}")

    def test_other_roles_are_forbidden(self):
        self.assertEqual(self.get(self.prof).status_code, 403)
        admin = User.objects.create_superuser("admin@example.com", "Admin", PASSWORD)
        self.assertEqual(self.get(admin).status_code, 403)

    def test_shows_my_groups_only(self):
        response = self.get()
        self.assertContains(response, "Welcome back, Ali")
        self.assertContains(response, "Group A")
        self.assertContains(response, "2 students")
        self.assertNotContains(response, "Group B")

    def test_pending_lists_open_unsubmitted_assignments_of_my_groups(self):
        self.assignment("Due tomorrow", days=1)
        self.assignment("Next week", days=7)
        self.assignment("Other group", group=self.other_group)
        self.assignment("Past deadline", days=-1)
        self.assignment("Closed", status=Assignment.Status.CLOSED)
        done = self.assignment("Already sent")
        Submission.objects.create(
            student=self.student, bug=self.bug, assignment=done, submitted_code="x"
        )

        pending = self.get().context["pending"]
        self.assertEqual([a.title for a in pending], ["Due tomorrow", "Next week"])
        self.assertTrue(pending[0].due_soon)
        self.assertFalse(pending[1].due_soon)

    def test_classmate_submission_does_not_hide_my_assignment(self):
        a = self.assignment("Shared")
        Submission.objects.create(student=self.other, bug=self.bug, assignment=a, submitted_code="x")
        self.assertContains(self.get(), "Shared")

    def test_recent_grades_show_only_my_graded_submissions(self):
        a = self.assignment("Graded one")
        Submission.objects.create(
            student=self.student, bug=self.bug, assignment=a, submitted_code="x",
            status=Submission.Status.GRADED, grade=9.5, feedback="Clean fix",
            graded_at=timezone.now(),
        )
        Submission.objects.create(
            student=self.other, bug=self.bug, assignment=a, submitted_code="y",
            status=Submission.Status.GRADED, grade=3, feedback="Omar feedback",
            graded_at=timezone.now(),
        )
        response = self.get()
        self.assertContains(response, "9.5")
        self.assertContains(response, "Clean fix")
        self.assertNotContains(response, "Omar feedback")
        self.assertEqual(response.context["graded_count"], 1)

    def test_empty_states(self):
        loner = User.objects.create_user("lina@example.com", "Lina", PASSWORD)
        response = self.get(loner)
        self.assertContains(response, "You are not in a group yet.")
        self.assertContains(response, "Nothing pending.")
        self.assertContains(response, "No grades yet.")

    def test_solution_code_is_never_shown(self):
        self.assignment("Due soon", days=1)
        self.assertNotContains(self.get(), self.bug.solution_code)


class AssignmentPagesTests(StudentTestCase):
    list_url = reverse("student:assignments_list")

    def detail(self, assignment, user=None):
        self.client.force_login(user or self.student)
        return self.client.get(reverse("student:assignment_detail", args=[assignment.pk]))

    def submit(self, assignment, student=None, **extra):
        return Submission.objects.create(
            student=student or self.student, bug=self.bug, assignment=assignment,
            submitted_code="fixed", **extra,
        )

    def list_statuses(self, query=""):
        self.client.force_login(self.student)
        response = self.client.get(self.list_url + query)
        return {a.title: a.my_status for a in response.context["assignments"]}

    def test_pages_need_a_student(self):
        a = self.assignment("Task")
        for url in (self.list_url, reverse("student:assignment_detail", args=[a.pk])):
            self.assertEqual(self.client.get(url).status_code, 302)
            self.client.force_login(self.prof)
            self.assertEqual(self.client.get(url).status_code, 403)
            self.client.logout()

    def test_list_shows_each_status_for_my_groups_only(self):
        self.assignment("Open")
        self.assignment("Past deadline", days=-1)
        self.assignment("Closed early", status=Assignment.Status.CLOSED)
        self.submit(self.assignment("Sent"))
        self.submit(
            self.assignment("Marked", days=-2),
            status=Submission.Status.GRADED, grade=7, graded_at=timezone.now(),
        )
        self.assignment("Other group", group=self.other_group)

        self.assertEqual(
            self.list_statuses(),
            {
                "Open": "todo",
                "Past deadline": "missed",
                "Closed early": "missed",
                "Sent": "submitted",
                "Marked": "graded",
            },
        )

    def test_status_filter_and_counts(self):
        self.assignment("Open")
        self.submit(self.assignment("Sent"))
        self.assertEqual(self.list_statuses("?status=todo"), {"Open": "todo"})
        self.assertEqual(self.list_statuses("?status=nonsense"), {"Open": "todo", "Sent": "submitted"})
        tabs = {t["key"]: t["count"] for t in self.client.get(self.list_url).context["tabs"]}
        self.assertEqual(tabs, {"": 2, "todo": 1, "submitted": 1, "graded": 0, "missed": 0})

    def test_assignment_in_two_of_my_groups_is_listed_once(self):
        self.other_group.students.add(self.student)
        a = self.assignment("Both groups")
        a.groups.add(self.other_group)
        self.assertEqual(self.list_statuses(), {"Both groups": "todo"})
        self.assertContains(self.detail(a), "Group A, Group B")

    def test_classmate_submission_does_not_change_my_status(self):
        a = self.assignment("Shared")
        self.submit(a, student=self.other, status=Submission.Status.GRADED, grade=10)
        self.assertEqual(self.list_statuses(), {"Shared": "todo"})

    def test_detail_shows_bug_without_solution(self):
        a = self.assignment("Task", instructions="Fix the loop bound.")
        response = self.detail(a)
        self.assertContains(response, "Fix the loop bound.")
        self.assertContains(response, self.bug.description)
        self.assertContains(response, self.bug.buggy_code)
        self.assertContains(response, "Not submitted yet.")
        self.assertNotContains(response, self.bug.solution_code)

    def test_detail_of_another_groups_assignment_is_404(self):
        a = self.assignment("Not mine", group=self.other_group)
        self.assertEqual(self.detail(a).status_code, 404)

    def test_detail_shows_my_grade_and_feedback_only(self):
        a = self.assignment("Task")
        self.submit(a, status=Submission.Status.GRADED, grade=8.5, feedback="Nice fix")
        self.submit(a, student=self.other, status=Submission.Status.GRADED, grade=2, feedback="Omar notes")
        response = self.detail(a)
        self.assertContains(response, "8.5")
        self.assertContains(response, "Nice fix")
        self.assertNotContains(response, "Omar notes")

    def test_detail_says_when_closed(self):
        self.assertContains(self.detail(self.assignment("Late", days=-1)), "This assignment is closed")
        self.assertNotContains(self.detail(self.assignment("Open")), "This assignment is closed")

    def test_dashboard_links_to_detail(self):
        a = self.assignment("Linked")
        self.assertContains(self.get(), reverse("student:assignment_detail", args=[a.pk]))


class WorkspaceTests(StudentTestCase):
    def ws_url(self, assignment):
        return reverse("student:assignment_workspace", args=[assignment.pk])

    def post(self, assignment, code="fixed = True\n", user=None):
        self.client.force_login(user or self.student)
        return self.client.post(self.ws_url(assignment), {"code": code})

    def my_submissions(self, assignment):
        return Submission.objects.filter(student=self.student, assignment=assignment)

    def test_needs_a_student_in_the_group(self):
        a = self.assignment("Task")
        self.assertEqual(self.client.get(self.ws_url(a)).status_code, 302)
        self.client.force_login(self.prof)
        self.assertEqual(self.client.get(self.ws_url(a)).status_code, 403)
        other = self.assignment("Not mine", group=self.other_group)
        self.assertEqual(self.post(other).status_code, 404)
        self.assertFalse(Submission.objects.exists())

    def test_editor_starts_with_buggy_code_and_hides_solution(self):
        a = self.assignment("Task")
        self.client.force_login(self.student)
        response = self.client.get(self.ws_url(a))
        self.assertContains(response, "Starting from the buggy code.")
        self.assertContains(response, "for i in range(len(x) - 1): pass</textarea>")
        self.assertNotContains(response, self.bug.solution_code)

    def test_submit_saves_the_fix_and_redirects(self):
        a = self.assignment("Task")
        response = self.post(a, code="line one\r\n    line two\r\n")
        self.assertRedirects(
            response, reverse("student:assignment_detail", args=[a.pk]),
            fetch_redirect_response=False,  # the flash message shows only once
        )
        submission = self.my_submissions(a).get()
        self.assertEqual(submission.submitted_code, "line one\n    line two\n")
        self.assertEqual(submission.bug, self.bug)
        self.assertEqual(submission.status, Submission.Status.SUBMITTED)
        self.assertContains(self.client.get(response["Location"]), "Fix submitted.")

    def test_editor_reloads_my_latest_fix(self):
        a = self.assignment("Task")
        self.post(a, code="first try")
        self.post(a, code="second try")
        self.assertEqual(self.my_submissions(a).count(), 2)
        response = self.client.get(self.ws_url(a))
        self.assertContains(response, "second try</textarea>")
        self.assertContains(response, "Loaded your last submission.")

    def test_empty_or_unchanged_code_is_rejected(self):
        a = self.assignment("Task")
        self.assertContains(self.post(a, code="   \n"), "Your fix is empty.")
        unchanged = self.bug.buggy_code.replace("\n", "\r\n") + "\n"
        self.assertContains(self.post(a, code=unchanged), "still the original buggy code")
        self.assertFalse(self.my_submissions(a).exists())

    def test_submit_after_deadline_is_blocked(self):
        a = self.assignment("Late", days=-1)
        response = self.post(a)
        self.assertRedirects(response, self.ws_url(a))
        self.assertFalse(self.my_submissions(a).exists())
        page = self.client.get(self.ws_url(a))
        self.assertContains(page, "The deadline has passed")
        self.assertContains(page, "readonly")
        self.assertContains(page, "disabled")

    def test_submit_to_closed_assignment_is_blocked(self):
        a = self.assignment("Closed", status=Assignment.Status.CLOSED)
        self.post(a)
        self.assertFalse(self.my_submissions(a).exists())

    def test_graded_work_cannot_be_resubmitted(self):
        a = self.assignment("Task")
        Submission.objects.create(
            student=self.student, bug=self.bug, assignment=a, submitted_code="done",
            status=Submission.Status.GRADED, grade=9,
        )
        self.post(a, code="sneaky change")
        self.assertEqual(self.my_submissions(a).count(), 1)
        self.assertContains(self.client.get(self.ws_url(a)), "already graded")

    def test_detail_page_solve_button(self):
        open_task = self.assignment("Open")
        self.client.force_login(self.student)
        detail = reverse("student:assignment_detail", args=[open_task.pk])
        self.assertContains(self.client.get(detail), "Solve this bug")
        late = self.assignment("Late", days=-1)
        page = self.client.get(reverse("student:assignment_detail", args=[late.pk]))
        self.assertNotContains(page, self.ws_url(late))


class PracticeTests(StudentTestCase):
    list_url = reverse("student:public_bugs")

    def setUp(self):
        super().setUp()
        self.public = self.make_bug("Public loop", language="python", difficulty=Bug.Difficulty.EASY)
        self.dart = self.make_bug("Dart null", language="Dart", difficulty=Bug.Difficulty.HARD)

    def make_bug(self, title, **extra):
        fields = {
            "description": f"{title} description",
            "buggy_code": "x = 1",
            "solution_code": "x = 2  # SOLUTION",
            "language": "python",
            "difficulty": Bug.Difficulty.MEDIUM,
            "visibility": Bug.Visibility.PUBLIC,
            "created_by": self.prof,
            **extra,
        }
        return Bug.objects.create(title=title, **fields)

    def ws_url(self, bug):
        return reverse("student:practice_workspace", args=[bug.pk])

    def titles(self, query=""):
        self.client.force_login(self.student)
        return [b.title for b in self.client.get(self.list_url + query).context["bugs"]]

    def test_pages_need_a_student(self):
        for url in (self.list_url, self.ws_url(self.public)):
            self.assertEqual(self.client.get(url).status_code, 302)
            self.client.force_login(self.prof)
            self.assertEqual(self.client.get(url).status_code, 403)
            self.client.logout()

    def test_list_shows_public_bugs_only(self):
        # self.bug from the base fixtures is private.
        self.assertEqual(self.titles(), ["Dart null", "Public loop"])

    def test_filters(self):
        self.assertEqual(self.titles("?language=dart"), ["Dart null"])
        self.assertEqual(self.titles("?difficulty=easy"), ["Public loop"])
        self.assertEqual(self.titles("?q=LOOP"), ["Public loop"])
        self.assertEqual(self.titles("?q=description&language=python&difficulty=hard"), [])
        self.assertEqual(self.titles("?difficulty=bogus"), ["Dart null", "Public loop"])
        response = self.client.get(self.list_url + "?q=nothing-matches")
        self.assertContains(response, "No bugs match these filters.")

    def test_language_options_are_case_insensitive_and_unique(self):
        self.make_bug("Another dart", language="dart")
        self.client.force_login(self.student)
        languages = list(self.client.get(self.list_url).context["languages"])
        self.assertEqual(languages, ["dart", "python"])

    def test_private_bug_cannot_be_practised(self):
        self.client.force_login(self.student)
        self.assertEqual(self.client.get(self.ws_url(self.bug)).status_code, 404)
        self.client.post(self.ws_url(self.bug), {"code": "changed"})
        self.assertFalse(Submission.objects.exists())

    def test_practice_attempt_is_saved_without_assignment_or_grade(self):
        self.client.force_login(self.student)
        response = self.client.post(self.ws_url(self.public), {"code": "x = 2"})
        self.assertRedirects(response, self.ws_url(self.public), fetch_redirect_response=False)
        attempt = Submission.objects.get()
        self.assertIsNone(attempt.assignment)
        self.assertIsNone(attempt.grade)
        self.assertTrue(attempt.is_practice)
        page = self.client.get(self.ws_url(self.public))
        self.assertContains(page, "Practice attempt saved.")
        self.assertContains(page, "x = 2</textarea>")
        self.assertNotContains(page, "SOLUTION")

    def test_attempt_count_is_mine_and_practice_only(self):
        Submission.objects.create(student=self.student, bug=self.public, submitted_code="a")
        Submission.objects.create(student=self.student, bug=self.public, submitted_code="b")
        Submission.objects.create(student=self.other, bug=self.public, submitted_code="c")
        a = self.assignment("Uses public bug")
        a.bug = self.public
        a.save()
        Submission.objects.create(student=self.student, bug=self.public, assignment=a, submitted_code="d")
        self.client.force_login(self.student)
        bugs = {b.title: b.my_attempts for b in self.client.get(self.list_url).context["bugs"]}
        self.assertEqual(bugs, {"Dart null": 0, "Public loop": 2})

    def test_practice_does_not_count_as_assignment_work(self):
        a = self.assignment("Task")
        Submission.objects.create(student=self.student, bug=self.bug, submitted_code="practice")
        self.client.force_login(self.student)
        statuses = {x.title: x.my_status for x in self.client.get(reverse("student:assignments_list")).context["assignments"]}
        self.assertEqual(statuses, {"Task": "todo"})

    def test_unchanged_code_is_rejected(self):
        self.client.force_login(self.student)
        self.assertContains(self.client.post(self.ws_url(self.public), {"code": "x = 1"}), "still the original buggy code")
        self.assertFalse(Submission.objects.exists())


class ResultsTests(StudentTestCase):
    results_url = reverse("student:results")

    def sub(self, student=None, assignment=None, **extra):
        return Submission.objects.create(
            student=student or self.student, bug=self.bug, assignment=assignment,
            submitted_code="code", **extra,
        )

    def graded(self, grade, feedback="", student=None, title="Task"):
        return self.sub(
            student=student, assignment=self.assignment(title),
            status=Submission.Status.GRADED, grade=grade, feedback=feedback,
            graded_at=timezone.now(),
        )

    def get_results(self, query=""):
        self.client.force_login(self.student)
        return self.client.get(self.results_url + query)

    def test_needs_a_student(self):
        self.assertEqual(self.client.get(self.results_url).status_code, 302)
        self.client.force_login(self.prof)
        self.assertEqual(self.client.get(self.results_url).status_code, 403)

    def test_empty_states(self):
        response = self.get_results()
        self.assertContains(response, "No grades yet.")
        self.assertContains(response, "Nothing submitted yet.")
        self.assertIsNone(response.context["average"])

    def test_grades_feedback_and_counts_are_mine_only(self):
        self.graded(8, "Line one\nLine two", title="First")
        self.graded(9, "Great", title="Second")
        self.graded(1, "Omar only", student=self.other, title="Omar task")
        self.sub(assignment=self.assignment("Waiting"))
        self.sub()  # practice
        response = self.get_results()
        self.assertEqual(response.context["average"], 8.5)
        self.assertEqual(response.context["waiting_count"], 1)
        self.assertEqual(response.context["practice_count"], 1)
        self.assertEqual(len(response.context["graded"]), 2)
        self.assertContains(response, "Line one<br>Line two")
        self.assertNotContains(response, "Omar only")
        self.assertEqual(response.context["history"].paginator.count, 4)

    def test_history_is_paginated(self):
        for _ in range(25):
            self.sub()
        first = self.get_results()
        self.assertEqual(len(first.context["history"]), 20)
        self.assertContains(first, "Page 1 of 2")
        self.assertEqual(len(self.get_results("?page=2").context["history"]), 5)
        self.assertEqual(self.get_results("?page=junk").context["history"].number, 1)

    def test_solution_code_is_never_shown(self):
        self.graded(7)
        self.assertNotContains(self.get_results(), self.bug.solution_code)

    def test_dashboard_links_to_results(self):
        self.assertContains(self.get(), self.results_url)
