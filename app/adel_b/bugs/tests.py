import json

from django.contrib.auth import get_user_model
from django.contrib.staticfiles import finders
from django.test import Client, TestCase

from .models import Attempt, Bug, Draft


def make_user(username="learner", **extra):
    return get_user_model().objects.create_user(
        username=username, email=f"{username}@example.com", password="debug-gym-pass", **extra
    )


class BugApiTests(TestCase):
    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_page_exercises_are_seeded(self):
        response = self.client.get("/api/bugs/")
        self.assertEqual(response.status_code, 200)
        ids = [bug["id"] for bug in response.json()["bugs"]]
        self.assertEqual(
            ids,
            [
                "remove-negatives",
                "total-starts-late",
                "duplicated-result",
                "missing-last-element",
                "count-words",
            ],
        )

    def test_only_workspace_bugs_have_a_workspace_url(self):
        bugs = {bug["id"]: bug for bug in self.client.get("/api/bugs/").json()["bugs"]}
        self.assertEqual(bugs["remove-negatives"]["workspaceUrl"], "http://localhost:8080")
        self.assertIsNone(bugs["count-words"]["workspaceUrl"])

    def test_bug_detail(self):
        response = self.client.get("/api/bugs/remove-negatives/")
        self.assertEqual(response.status_code, 200)
        bug = response.json()["bug"]
        self.assertEqual(bug["title"], "The surviving negative")
        self.assertIn("numbers.remove(number)", bug["buggyCode"])

    def test_unknown_bug_returns_404(self):
        response = self.client.get("/api/bugs/missing/")
        self.assertEqual(response.status_code, 404)

    def test_create_bug_needs_staff(self):
        self.client.force_login(make_user())
        response = self.client.post(
            "/api/bugs/",
            data=json.dumps({"slug": "x", "title": "X", "description": "X"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)

    def test_create_bug(self):
        self.client.force_login(make_user(is_staff=True))
        response = self.client.post(
            "/api/bugs/",
            data=json.dumps({
                "slug": "off-by-one",
                "title": "One step too far",
                "description": "A loop reads past the end of the list.",
                "topic": "Indexes",
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["bug"]["id"], "off-by-one")
        self.assertTrue(Bug.objects.filter(slug="off-by-one").exists())

    def test_create_rejects_missing_fields(self):
        self.client.force_login(make_user(is_staff=True))
        response = self.client.post(
            "/api/bugs/", data=json.dumps({"slug": "x"}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_create_rejects_duplicate_slug(self):
        self.client.force_login(make_user(is_staff=True))
        response = self.client.post(
            "/api/bugs/",
            data=json.dumps({
                "slug": "remove-negatives",
                "title": "Again",
                "description": "Duplicate.",
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 409)

    def test_create_rejects_bad_json(self):
        self.client.force_login(make_user(is_staff=True))
        response = self.client.post(
            "/api/bugs/", data="not json", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)


class PageAndMatchTests(TestCase):
    def test_index_page_loads_the_two_screens(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="view-new"')
        self.assertContains(response, 'id="view-practice"')
        self.assertContains(response, "/static/bugs/app.js")

    def test_page_assets_are_found(self):
        self.assertIsNotNone(finders.find("bugs/app.js"))
        self.assertIsNotNone(finders.find("bugs/styles.css"))

    def test_match_list_mutation_query(self):
        response = self.client.post(
            "/api/exercises",
            data=json.dumps({"query": "A Python list mutation bug with negative numbers"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["exercise"]["id"], "remove-negatives")

    def test_match_dictionary_query(self):
        response = self.client.post(
            "/api/exercises",
            data=json.dumps({"query": "counting words in a dictionary"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["exercise"]["id"], "count-words")

    def test_match_unknown_query_returns_404(self):
        response = self.client.post(
            "/api/exercises",
            data=json.dumps({"query": "javascript promise deadlock"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)

    def test_match_rejects_non_text_query(self):
        response = self.client.post(
            "/api/exercises", data=json.dumps({"query": 5}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)


class DraftApiTests(TestCase):
    url = "/api/bugs/remove-negatives/draft/"

    def setUp(self):
        self.client.force_login(make_user())

    def test_needs_login(self):
        self.client.logout()
        self.assertEqual(self.client.get(self.url).status_code, 401)

    def test_drafts_are_private(self):
        self.put({"code": "mine\n"})
        self.client.force_login(make_user("other"))
        self.assertIsNone(self.client.get(self.url).json()["draft"])

    def put(self, payload):
        return self.client.put(self.url, data=json.dumps(payload), content_type="application/json")

    def test_no_draft_at_first(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.json()["draft"])

    def test_save_and_load_draft(self):
        code = "def remove_negatives(numbers):\n    return [n for n in numbers if n >= 0]\n"
        self.assertEqual(self.put({"code": code}).status_code, 200)
        self.assertEqual(self.put({"code": code + "# again\n"}).status_code, 200)
        self.assertEqual(Draft.objects.count(), 1)
        draft = self.client.get(self.url).json()["draft"]
        self.assertEqual(draft["code"], code + "# again\n")
        self.assertEqual(draft["bugId"], "remove-negatives")

    def test_delete_resets_draft(self):
        self.put({"code": "pass\n"})
        self.assertEqual(self.client.delete(self.url).status_code, 200)
        self.assertIsNone(self.client.get(self.url).json()["draft"])

    def test_rejects_non_text_code(self):
        self.assertEqual(self.put({"code": 5}).status_code, 400)

    def test_rejects_huge_code(self):
        self.assertEqual(self.put({"code": "x" * 50_001}).status_code, 400)

    def test_unknown_bug_returns_404(self):
        response = self.client.get("/api/bugs/missing/draft/")
        self.assertEqual(response.status_code, 404)


class AttemptAndHistoryTests(TestCase):
    url = "/api/bugs/remove-negatives/attempts/"

    def setUp(self):
        self.client.force_login(make_user())

    def test_needs_login(self):
        self.client.logout()
        self.assertEqual(self.submit(3).status_code, 401)
        self.assertEqual(self.client.get("/api/history/").status_code, 401)

    def test_history_is_private(self):
        self.submit(3)
        self.client.force_login(make_user("other"))
        self.assertEqual(self.client.get("/api/history/").json(), {"items": [], "activity": []})
        self.assertEqual(self.client.get(self.url).json(), {"attempts": []})

    def submit(self, passed, total=3, code="def remove_negatives(numbers):\n    return numbers\n"):
        return self.client.post(
            self.url,
            data=json.dumps({"code": code, "passed": passed, "total": total}),
            content_type="application/json",
        )

    def test_failed_attempt_is_saved(self):
        response = self.submit(1)
        self.assertEqual(response.status_code, 201)
        attempt = response.json()["attempt"]
        self.assertEqual((attempt["passed"], attempt["total"], attempt["solved"]), (1, 3, False))
        self.assertEqual(Attempt.objects.count(), 1)

    def test_passing_attempt_is_solved(self):
        self.assertTrue(self.submit(3).json()["attempt"]["solved"])

    def test_list_attempts_newest_first(self):
        self.submit(1)
        self.submit(3)
        attempts = self.client.get(self.url).json()["attempts"]
        self.assertEqual([attempt["passed"] for attempt in attempts], [3, 1])

    def test_rejects_wrong_test_count(self):
        self.assertEqual(self.submit(2, total=2).status_code, 400)

    def test_rejects_passed_above_total(self):
        self.assertEqual(self.submit(4).status_code, 400)

    def test_rejects_non_integer_counts(self):
        self.assertEqual(self.submit("3").status_code, 400)
        self.assertEqual(self.submit(True).status_code, 400)

    def test_unknown_bug_returns_404(self):
        response = self.client.post(
            "/api/bugs/missing/attempts/",
            data=json.dumps({"code": "", "passed": 0, "total": 0}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)

    def test_history_is_empty_at_first(self):
        self.assertEqual(self.client.get("/api/history/").json(), {"items": [], "activity": []})

    def test_history_statuses(self):
        self.client.put(
            "/api/bugs/count-words/draft/",
            data=json.dumps({"code": "pass\n"}),
            content_type="application/json",
        )
        self.submit(1)
        self.client.post(
            "/api/bugs/total-starts-late/attempts/",
            data=json.dumps({"code": "", "passed": 3, "total": 3}),
            content_type="application/json",
        )
        body = self.client.get("/api/history/").json()
        statuses = {item["bugId"]: item["status"] for item in body["items"]}
        self.assertEqual(
            statuses,
            {"count-words": "progress", "remove-negatives": "failed", "total-starts-late": "solved"},
        )
        self.assertEqual(body["items"][0]["bugId"], "total-starts-late")
        self.assertEqual(len(body["activity"]), 2)

    def test_one_solve_keeps_bug_solved(self):
        self.submit(3)
        self.submit(1)
        items = self.client.get("/api/history/").json()["items"]
        self.assertEqual(items[0]["status"], "solved")


class CsrfTests(TestCase):
    def test_changes_need_the_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(make_user())
        url = "/api/bugs/remove-negatives/draft/"
        body = json.dumps({"code": "pass\n"})
        self.assertEqual(client.put(url, data=body, content_type="application/json").status_code, 403)

        client.get("/")  # the page hands out the CSRF cookie
        token = client.cookies["csrftoken"].value
        response = client.put(url, data=body, content_type="application/json", HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, 200)


class TestEditTests(TestCase):
    url = "/api/bugs/remove-negatives/tests/1/"

    def setUp(self):
        self.client.force_login(make_user())

    def edit(self, input_text, expected_text, url=None):
        return self.client.put(
            url or self.url,
            data=json.dumps({"input": input_text, "expected": expected_text}),
            content_type="application/json",
        )

    def draft(self):
        return self.client.get("/api/bugs/remove-negatives/draft/").json()["draft"]

    def test_edit_one_test(self):
        response = self.edit("[7, -1, -2]", "[7]")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body["edited"])
        self.assertEqual(body["tests"][1], {"name": "Mixed numbers", "input": [7, -1, -2], "expected": [7]})
        self.assertEqual(body["tests"][0]["input"], [])
        self.assertEqual(self.draft()["tests"], body["tests"])
        self.assertEqual(Bug.objects.get(slug="remove-negatives").tests[1]["input"], [4, -3, -2, 5])

    def test_python_values_are_read_safely(self):
        response = self.edit("{'apple': 2, 'pear': None}", "'it\\'s'", url="/api/bugs/count-words/tests/0/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["tests"][0]["input"], {"apple": 2, "pear": None})
        self.assertEqual(response.json()["tests"][0]["expected"], "it's")

    def test_rejects_code_and_unsupported_values(self):
        for bad in ("__import__('os')", "[1, 2", "(1, 2)", "{1: 2}", "", "1e999", "x" * 2001):
            response = self.edit(bad, "[]")
            self.assertEqual(response.status_code, 400, bad)
            self.assertIn("input", response.json()["fields"])
        self.assertIsNone(self.draft())

    def test_restore_original(self):
        self.edit("[7, -1]", "[7]")
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["edited"])
        self.assertIsNone(self.draft()["tests"])

    def test_saving_the_original_values_is_not_an_edit(self):
        response = self.edit("[4, -3, -2, 5]", "[4, 5]")
        self.assertFalse(response.json()["edited"])
        self.assertIsNone(self.draft())

    def test_unknown_test_returns_404(self):
        self.assertEqual(self.edit("[]", "[]", url="/api/bugs/remove-negatives/tests/3/").status_code, 404)

    def test_needs_login(self):
        self.client.logout()
        self.assertEqual(self.edit("[]", "[]").status_code, 401)

    def test_code_edits_keep_edited_tests(self):
        self.edit("[7, -1]", "[7]")
        self.client.put(
            "/api/bugs/remove-negatives/draft/",
            data=json.dumps({"code": "changed\n"}),
            content_type="application/json",
        )
        self.assertEqual(self.draft()["tests"][1]["input"], [7, -1])

    def test_reset_code_keeps_edited_tests(self):
        self.client.put(
            "/api/bugs/remove-negatives/draft/",
            data=json.dumps({"code": "changed\n"}),
            content_type="application/json",
        )
        self.edit("[7, -1]", "[7]")
        response = self.client.delete("/api/bugs/remove-negatives/draft/")
        draft = response.json()["draft"]
        self.assertIn("numbers.remove(number)", draft["code"])
        self.assertEqual(draft["tests"][1]["input"], [7, -1])
