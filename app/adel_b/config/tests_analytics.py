import json
import queue
import uuid
from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from accounts.models import Profile
from config import analytics

URL = "https://analytics.example.test/events"


class LearnerIdTests(TestCase):
    def test_id_is_a_random_uuid_unrelated_to_the_account(self):
        user = get_user_model().objects.create_user(
            username="ada-lovelace", email="ada@university.example"
        )
        learner = analytics.learner_id(user)

        self.assertEqual(uuid.UUID(learner).version, 4)
        self.assertEqual(learner, analytics.learner_id(user))
        for personal in (user.username, user.email):
            self.assertNotIn(personal, learner)
        # A short id can appear inside random hex by chance, so compare whole values.
        self.assertNotEqual(learner, str(user.pk))

    def test_each_learner_has_their_own_id(self):
        users = get_user_model().objects
        first = analytics.learner_id(users.create_user(username="one"))
        second = analytics.learner_id(users.create_user(username="two"))
        self.assertNotEqual(first, second)

    def test_a_learner_without_a_profile_gets_one(self):
        user = get_user_model().objects.create_user(username="no-profile")
        Profile.objects.filter(user=user).delete()
        self.assertEqual(len(analytics.learner_id(user)), 32)


class BuildEventTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="builder", email="builder@university.example"
        )

    def test_event_carries_the_registry_fields_and_no_personal_data(self):
        event = analytics.build_event("exercise_opened", self.user, exercise_slug="remove-negatives")

        self.assertEqual(
            set(event), {"name", "timestamp", "learner_id", "source", "exercise_slug"}
        )
        self.assertEqual(event["source"], "web")
        self.assertEqual(event["learner_id"], analytics.learner_id(self.user))
        self.assertNotIn("builder", json.dumps(event))

    def test_source_is_a_closed_set(self):
        for source in analytics.SOURCES:
            analytics.build_event("exercise_searched", self.user, source=source, result_count=0)
        with self.assertRaises(ValueError):
            analytics.build_event("exercise_searched", self.user, source="mobile", result_count=0)

    def test_the_registry_is_enforced(self):
        bad_calls = (
            ("unknown_event", {}),
            ("exercise_opened", {}),
            ("exercise_opened", {"exercise_slug": "x", "email": "a@b.example"}),
            ("exercise_searched", {"result_count": True}),
            ("exercise_searched", {"result_count": "3"}),
            ("solution_verified", {
                "exercise_slug": "x", "passed_count": 1, "total_count": 2, "all_passed": 0,
            }),
        )
        for name, fields in bad_calls:
            with self.subTest(name=name, fields=fields), self.assertRaises(ValueError):
                analytics.build_event(name, self.user, **fields)

    def test_an_anonymous_visitor_has_no_event(self):
        anonymous = MagicMock(is_authenticated=False)
        with self.assertRaises(ValueError):
            analytics.build_event("exercise_searched", anonymous, result_count=1)


@override_settings(DEBUG_GYM_ANALYTICS_URL=URL, DEBUG_GYM_ANALYTICS_KEY="test-key")
class EmitTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="emitter")

    def test_a_configured_event_is_delivered_with_its_credential(self):
        with patch.object(analytics, "_post") as post:
            queued = analytics.emit(
                "solution_verified", self.user,
                exercise_slug="remove-negatives", passed_count=3, total_count=3, all_passed=True,
            )
            analytics.flush()

        self.assertTrue(queued)
        url, key, event = post.call_args.args
        self.assertEqual((url, key), (URL, "test-key"))
        self.assertEqual(event["name"], "solution_verified")
        self.assertIs(event["all_passed"], True)
        self.assertEqual(event["learner_id"], analytics.learner_id(self.user))

    def test_the_post_is_json_with_a_bearer_key_and_a_timeout(self):
        event = {"name": "exercise_searched", "result_count": 1}
        with patch("config.analytics.urllib.request.urlopen") as urlopen:
            analytics._post(URL, "test-key", event)

        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, URL)
        self.assertEqual(request.get_header("Authorization"), "Bearer test-key")
        self.assertEqual(request.get_header("Content-type"), "application/json")
        self.assertEqual(json.loads(request.data), event)
        self.assertEqual(urlopen.call_args.kwargs["timeout"], analytics.SEND_TIMEOUT_SECONDS)

    def test_a_failing_backend_never_reaches_the_caller(self):
        with patch.object(analytics, "_post", side_effect=OSError("down")):
            with self.assertLogs("debug_gym.analytics", level="WARNING") as logs:
                queued = analytics.emit("exercise_searched", self.user, result_count=2)
                analytics.flush()

        self.assertTrue(queued)
        self.assertIn("was not delivered", logs.output[0])

    def test_a_malformed_event_is_logged_and_not_raised(self):
        with self.assertLogs("debug_gym.analytics", level="WARNING"):
            self.assertFalse(analytics.emit("exercise_searched", self.user, result_count="x"))

    def test_a_full_queue_drops_the_event_without_raising(self):
        with patch.object(analytics, "_queue", queue.Queue(maxsize=1)), \
                patch.object(analytics, "_ensure_worker"):
            self.assertTrue(analytics.emit("exercise_searched", self.user, result_count=1))
            with self.assertLogs("debug_gym.analytics", level="WARNING") as logs:
                self.assertFalse(analytics.emit("exercise_searched", self.user, result_count=1))
        self.assertIn("queue is full", logs.output[0])


class CollectionOffTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="quiet")

    @override_settings(DEBUG_GYM_ANALYTICS_URL="")
    def test_nothing_is_sent_when_unconfigured(self):
        with patch.object(analytics, "_post") as post:
            self.assertFalse(analytics.emit("exercise_searched", self.user, result_count=1))
            analytics.flush()
        post.assert_not_called()

    @override_settings(DEBUG_GYM_ANALYTICS_URL="http://analytics.example.test/events")
    def test_a_plain_http_address_keeps_collection_off(self):
        with patch.object(analytics, "_post") as post:
            with self.assertLogs("debug_gym.analytics", level="WARNING"):
                self.assertFalse(analytics.emit("exercise_searched", self.user, result_count=1))
            analytics.flush()
        post.assert_not_called()
