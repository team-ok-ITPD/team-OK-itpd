# [Professor Dev] Live catalog, assignment dialog, creation tabs and provider routing
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse

from core.agents import ask_agent, save_key
from core.models import AgentCredential, Assignment, Bug
from professor import tests as workflow


class CatalogUITests(TestCase):
    setUp = workflow.TeachingWorkflowTests.setUp
    assignment = workflow.TeachingWorkflowTests.assignment

    def test_visibility_owner_combinations_are_scoped_on_server(self):
        own_public = Bug.objects.create(title="Own public", created_by=self.teacher, visibility="public", language="python")
        expected = {
            ("all", "all"): {self.bug.pk, self.public.pk, own_public.pk},
            ("all", "my"): {self.bug.pk, own_public.pk},
            ("all", "others"): {self.public.pk},
            ("private", "all"): {self.bug.pk}, ("private", "my"): {self.bug.pk},
            ("private", "others"): set(),
            ("public", "all"): {self.public.pk, own_public.pk},
            ("public", "my"): {own_public.pk}, ("public", "others"): {self.public.pk},
        }
        for (visibility, owner), ids in expected.items():
            response = self.client.get(reverse("professor:bugs"), {
                "visibility": visibility, "owner": owner, "fragment": "1",
            })
            self.assertEqual({bug.pk for bug in response.context["bugs"]}, ids)
            self.assertNotContains(response, "<html")
        page = self.client.get(reverse("professor:bugs"))
        self.assertContains(page, 'name="visibility"')
        self.assertContains(page, 'name="owner"')
        self.assertNotContains(page, 'name="scope"')
        self.assertNotContains(page, '>Filter</button>')
        self.assertNotContains(page, 'id="catalog-assignment"')
        self.assertNotContains(page, 'data-assign-url=')
        for bug in (self.bug, self.public, own_public):
            details = self.client.get(reverse("professor:bug", args=[bug.pk]))
            self.assertContains(details, reverse("professor:catalog-assign", args=[bug.pk]))
            self.assertContains(details, 'id="catalog-assignment"')
            self.assertEqual(details.content.decode().count('id="catalog-assignment"'), 1)
            self.assertContains(details, 'Assign to a group')

    def test_modal_assign_creates_copy_with_tests_and_optional_deadline(self):
        self.public.tests_code = "def test_legacy(): assert False"
        self.public.save()
        url = reverse("professor:catalog-assign", args=[self.public.pk])
        self.assertEqual(self.client.get(url).status_code, 405)
        response = self.client.post(url, {"group": self.group.pk, "deadline": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["redirect"], reverse("professor:group", args=[self.group.pk]))
        assignment = Assignment.objects.get()
        self.assertIsNone(assignment.deadline)
        self.assertNotEqual(assignment.bug_id, self.public.pk)
        self.assertEqual(assignment.bug.visibility, "private")
        self.assertEqual(assignment.bug.created_by, self.teacher)
        self.assertEqual(assignment.bug.tests_code, self.public.tests_code)
        self.assertIn(reverse("professor:bug", args=[self.public.pk]), assignment.bug.description)

    def test_modal_rejects_foreign_group_private_bug_invalid_deadline_and_missing_csrf(self):
        url = reverse("professor:catalog-assign", args=[self.bug.pk])
        for data in ({"group": self.foreign_group.pk}, {"group": self.group.pk, "deadline": "bad"}, {}):
            self.assertEqual(self.client.post(url, data).status_code, 400)
        private = reverse("professor:catalog-assign", args=[self.foreign_bug.pk])
        self.assertEqual(self.client.post(private, {"group": self.group.pk}).status_code, 404)
        from django.test import Client
        csrf = Client(enforce_csrf_checks=True)
        csrf.force_login(self.teacher)
        self.assertEqual(csrf.post(url, {"group": self.group.pk}).status_code, 403)
        self.assertFalse(Assignment.objects.exists())

    def test_modal_updates_only_owned_group_assignment(self):
        assignment = self.assignment()
        response = self.client.post(reverse("professor:catalog-assign", args=[self.bug.pk]), {
            "group": self.group.pk, "deadline": "2027-01-01T12:00",
        })
        self.assertEqual(response.status_code, 200)
        assignment.refresh_from_db()
        self.assertIsNotNone(assignment.deadline)
        self.assertEqual(Assignment.objects.count(), 1)

    def test_create_tabs_keep_generation_validation_on_generation_tab(self):
        page = self.client.get(reverse("professor:create"))
        self.assertContains(page, 'role="tablist"')
        self.assertContains(page, 'id="generate-panel" role="tabpanel" aria-labelledby="generate-tab" hidden')
        response = self.client.post(reverse("professor:generate"), {"prompt": ""})
        self.assertEqual(response.context["active_tab"], "generate")
        self.assertContains(response, 'id="upload-panel" role="tabpanel" aria-labelledby="upload-tab" hidden')

    @patch("core.agents.urlopen")
    def test_provider_routes_key_and_clear_restores_platform(self, call):
        with TemporaryDirectory() as directory, override_settings(
            DEBUG_GYM_KEY_FILE=Path(directory)/"key", DEBUG_GYM_AGENT_KEY="platform-only",
            DEBUG_GYM_AGENT_URL="https://configured.example/chat", DEBUG_GYM_AGENT_MODEL="gpt-4.1-mini",
        ):
            call.return_value.__enter__.return_value.read.return_value = json.dumps({
                "choices": [{"message": {"content": '{"ok": true}'}}],
            }).encode()
            for provider, endpoint in (("openai", "https://api.openai.com/v1/chat/completions"),
                                       ("openrouter", "https://openrouter.ai/api/v1/chat/completions")):
                response = self.client.post(reverse("professor:settings"), {"key": "personal-only", "provider": provider})
                self.assertEqual(response.status_code, 302)
                self.assertEqual(AgentCredential.objects.get(user=self.teacher).provider, provider)
                ask_agent(self.teacher, "Generate", {})
                request = call.call_args.args[0]
                self.assertEqual(request.full_url, endpoint)
                self.assertEqual(request.get_header("Authorization"), "Bearer personal-only")
                if provider == "openrouter":
                    self.assertEqual(json.loads(request.data)["model"], "openai/gpt-4.1-mini")
                page = self.client.get(reverse("professor:settings"))
                self.assertContains(page, f'value="{provider}" selected')
                self.assertNotContains(page, "personal-only")
            self.client.post(reverse("professor:settings"), {"key": "", "provider": "openrouter"})
            ask_agent(self.teacher, "Generate", {})
            self.assertEqual(call.call_args.args[0].full_url, "https://configured.example/chat")
            self.assertEqual(call.call_args.args[0].get_header("Authorization"), "Bearer platform-only")
            self.assertFalse(AgentCredential.objects.filter(user=self.teacher).exists())
            invalid = self.client.post(reverse("professor:settings"), {"key": "rejected", "provider": "unknown"})
            self.assertIn("provider", invalid.context["form"].errors)
