# [Backend Dev] App configuration for the core app
import sys

from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "core"
    verbose_name = "Core"

    def ready(self):
        # Development server only: let VS Code containers reach it (core/bridge.py).
        from .bridge import start_with_runserver

        start_with_runserver(sys.argv)
