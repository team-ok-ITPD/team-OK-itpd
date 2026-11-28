from unittest.mock import patch

from django.test import SimpleTestCase, override_settings

from . import bridge


class IdeServerAddressTests(SimpleTestCase):
    @override_settings(DEBUG_GYM_IDE_SERVER_URL="http://localhost:8123")
    @patch.dict("os.environ", {"DEBUG_GYM_IDE_SERVER_URL": "http://localhost:8123"})
    def test_loopback_server_is_rewritten_for_code_server(self):
        self.assertEqual(bridge.ide_server_url(8000), "http://host.docker.internal:8123")

    @override_settings(DEBUG_GYM_IDE_SERVER_URL="http://host.docker.internal:8000")
    @patch.dict("os.environ", {}, clear=True)
    def test_default_uses_the_actual_request_port(self):
        self.assertEqual(bridge.ide_server_url(8011), "http://host.docker.internal:8011")

    @patch.dict("os.environ", {"DEBUG_GYM_IDE_SERVER_URL": "http://localhost:8123"})
    @patch("core.bridge.ensure_relay", return_value=True)
    def test_relay_uses_configured_server_port(self, relay):
        self.assertTrue(bridge.ensure_ide_relay(8000))
        relay.assert_called_once_with(8123)

    @patch.dict("os.environ", {"DEBUG_GYM_IDE_SERVER_URL": "https://gym.example.edu"})
    @patch("core.bridge.ensure_relay")
    def test_public_server_url_does_not_start_a_relay(self, relay):
        self.assertFalse(bridge.ensure_ide_relay(8000))
        relay.assert_not_called()
