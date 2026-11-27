# [Professor Dev] Additive local demo data with actual Docker test results
from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from core.models import Assignment, Bug, StudyGroup, Submission, User
from core.runtime import verify

PASSWORD = "DebugGym-Demo-2026!"
PYTHON_BUG = "def count_zeros(items):\n    return items[1:].count(0)\n"
PYTHON_FIX = "def count_zeros(items):\n    return items.count(0)\n"
PYTHON_TESTS = """from main import count_zeros
def test_first_zero():
    assert count_zeros([0, 1, 0]) == 2
def test_no_zeros():
    assert count_zeros([1, 2]) == 0
"""
JS_BUG = "module.exports = items => items.slice(1).filter(x => x === 0).length;\n"
JS_FIX = "module.exports = items => items.filter(x => x === 0).length;\n"
JS_TESTS = """const test = require('node:test');
const assert = require('node:assert/strict');
const count = require('./main');
test('first zero', () => assert.equal(count([0, 1, 0]), 2));
test('no zeros', () => assert.equal(count([1, 2]), 0));
"""


class Command(BaseCommand):
    help = "Add local teaching demo groups, exercises and verified submissions without resetting data."

    def add_arguments(self, parser):
        parser.add_argument("--teacher", default="teacher@debuggym.local")

    def handle(self, *args, **options):
        teacher = User.objects.filter(email=options["teacher"], role="professor").first()
        if teacher is None:
            raise CommandError("Create or select the professor account with --teacher first.")
        python = Bug(
            title="Demo · The forgotten zero", description="Count all zeros, including the first item.",
            language="python", entry_file="main.py", difficulty="easy", visibility="private",
            created_by=teacher, buggy_code=PYTHON_BUG,
            project_files={"main.py": PYTHON_BUG, "test_main.py": PYTHON_TESTS},
        )
        javascript = Bug(
            title="Demo · JavaScript zero counter", description="Investigate why the first element is skipped.",
            language="javascript", entry_file="main.js", difficulty="easy", visibility="public",
            created_by=teacher, buggy_code=JS_BUG,
            project_files={"main.js": JS_BUG, "main.test.js": JS_TESTS},
        )
        python = Bug.objects.filter(title=python.title, created_by=teacher).first() or python
        javascript = Bug.objects.filter(title=javascript.title, created_by=teacher).first() or javascript
        # Run real tests before writing demo data, so fixture scores are observed results.
        scores = {
            "fixed": verify(python, PYTHON_FIX), "buggy": verify(python, python.buggy_code),
            "js_fixed": verify(javascript, JS_FIX),
            "js_buggy": verify(javascript, javascript.buggy_code),
        }
        credentials = []
        with transaction.atomic():
            def demo_user(email, name, role="student"):
                user, created = User.objects.get_or_create(
                    email=email, defaults={"name": name, "role": role},
                )
                if created:
                    user.set_password(PASSWORD)
                    user.save()
                if user.role != role:
                    raise CommandError(f"The existing demo account {email} has a different role.")
                credentials.append((role, email, PASSWORD if created else "Existing password retained"))
                return user

            alice = demo_user("demo.alice@example.test", "Alice Demo")
            bob = demo_user("demo.bob@example.test", "Bob Demo")
            charlie = demo_user("demo.charlie@example.test", "Charlie Demo")
            other = demo_user("demo.other-teacher@example.test", "Demo Other Teacher", "professor")
            demo_user("demo.admin@example.test", "Demo Administrator", "admin")
            group, _ = StudyGroup.objects.get_or_create(
                name="Demo · Python foundations", professor=teacher,
                defaults={"description": "Three students with different debugging outcomes."},
            )
            group.students.add(alice, bob, charlie)
            advanced, _ = StudyGroup.objects.get_or_create(
                name="Demo · JavaScript lab", professor=teacher,
                defaults={"description": "A second group with independent assignments."},
            )
            advanced.students.add(alice, charlie)
            hidden, _ = StudyGroup.objects.get_or_create(
                name="Demo · Another teacher's group", professor=other,
            )
            hidden.students.add(bob)
            for example in (python, javascript):
                row, _ = Bug.objects.get_or_create(
                    title=example.title, created_by=teacher,
                    defaults={
                        "description": example.description, "language": example.language,
                        "entry_file": example.entry_file, "difficulty": example.difficulty,
                        "visibility": example.visibility, "buggy_code": example.buggy_code,
                        "project_files": example.project_files,
                    },
                )
                example.pk = row.pk
            for title, bug, target, due, status in (
                ("Demo · Past deadline", python, group, timezone.now() - timedelta(days=2), "active"),
                ("Demo · Due next week", python, group, timezone.now() + timedelta(days=7), "active"),
                ("Demo · Open practice assignment", javascript, advanced, None, "active"),
                ("Demo · Manually closed assignment", javascript, advanced, None, "closed"),
            ):
                assignment, _ = Assignment.objects.get_or_create(
                    title=title, professor=teacher,
                    defaults={"bug": bug, "deadline": due, "status": status},
                )
                assignment.groups.add(target)
                if title.endswith(("Past deadline", "Manually closed assignment")):
                    for student, fixed in ((alice, True), (bob if target == group else charlie, False)):
                        key = ("js_" if bug.language == "javascript" else "") + ("fixed" if fixed else "buggy")
                        passed, total = scores[key]
                        Submission.objects.get_or_create(
                            assignment=assignment, student=student, bug=bug,
                            submitted_code=(PYTHON_FIX if bug.language == "python" else JS_FIX) if fixed else bug.buggy_code,
                            defaults={"tests_passed": passed, "tests_total": total},
                        )
        path = settings.BASE_DIR / "DEMO_ACCOUNTS.md"
        lines = [
            "# Local v2 Demo Accounts", "", f"Main teacher: {teacher.email} (existing password).", "",
            "| Role | Email | Password |", "| --- | --- | --- |",
        ]
        lines.extend(f"| {role} | {email} | {password} |" for role, email, password in credentials)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        self.stdout.write(self.style.SUCCESS(f"Demo ready. Observed test counts: {scores}. Logins: {path}"))
