# [Professor Dev] Background worker for one-time post-deadline reviews
import time

from django.core.management.base import BaseCommand
from django.db import close_old_connections

from professor.reviews import review_due_assignments


class Command(BaseCommand):
    help = "Review due assignments once each. Runs every 30 seconds unless --once is passed."

    def add_arguments(self, parser):
        parser.add_argument("--once", action="store_true")

    def handle(self, *args, **options):
        while True:
            review_due_assignments()
            if options["once"]:
                return
            close_old_connections()
            time.sleep(30)
