"""Create demo accounts and progress for showing Debug GYM to a customer.

Running it again resets the demo: demo accounts, their exercises and their work are
deleted and recreated with new passwords. Nothing else in the database is touched.
"""

import datetime
import secrets
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from accounts.models import Profile
from bugs.models import Assignment, Attempt, Bug, Draft

User = get_user_model()
DOMAIN = "debuggym.demo"
WORDS = ["river", "cobalt", "maple", "orbit", "lantern", "canyon", "velvet", "harbor", "falcon", "meadow", "quartz", "ember"]

# username, role, display name, what this account shows in the demo
ACCOUNTS = [
    ("demo_admin", "admin", "Demo Admin", "Django admin: change any user's role (student or professor)."),
    ("prof_lina", Profile.PROFESSOR, "Prof. Lina", "Teaching pages: her 2 exercises, assignments and student progress."),
    ("student_ali", Profile.STUDENT, "Ali", "A student who solved both assignments and has a streak."),
    ("student_maria", Profile.STUDENT, "Maria", "A student in the middle: one in progress, one submitted but not solved (overdue)."),
    ("student_omar", Profile.STUDENT, "Omar", "A student who has not started: two open assignments, one overdue."),
]

EXERCISES = [
    {
        "slug": "demo-forgotten-zero",
        "title": "The forgotten zero",
        "summary": "Counting zeros misses the first one.",
        "description": "count_zeros() should count every 0 in the list, but the first element is never checked.",
        "difficulty": "Easy",
        "category": "arrays",
        "topic": "Arrays & loops",
        "duration": "10–15 min",
        "function_name": "count_zeros",
        "file_name": "count_zeros.py",
        "buggy_code": 'def count_zeros(numbers):\n    """Return how many zeros the list contains."""\n    return numbers[1:].count(0)\n',
        "fixed_code": 'def count_zeros(numbers):\n    """Return how many zeros the list contains."""\n    return numbers.count(0)\n',
        "symptom": "Wrong result · no exception raised",
        "tests": [
            {"name": "No zeros", "input": [1, 2, 3], "expected": 0},
            {"name": "Zero first", "input": [0, 1, 0], "expected": 2},
            {"name": "Only zeros", "input": [0, 0], "expected": 2},
        ],
        "due_in_days": 7,
    },
    {
        "slug": "demo-shrinking-word",
        "title": "The shrinking word",
        "summary": "Shouting a word loses its last letter.",
        "description": "shout() should return the word in capital letters followed by '!', but the last letter disappears.",
        "difficulty": "Easy",
        "category": "strings",
        "topic": "Strings",
        "duration": "5–10 min",
        "function_name": "shout",
        "file_name": "shout.py",
        "buggy_code": 'def shout(word):\n    """Return the word in capitals, followed by \'!\'."""\n    return word[:-1].upper() + "!"\n',
        "fixed_code": 'def shout(word):\n    """Return the word in capitals, followed by \'!\'."""\n    return word.upper() + "!"\n',
        "symptom": "Wrong result · no exception raised",
        "tests": [
            {"name": "One letter", "input": "a", "expected": "A!"},
            {"name": "A word", "input": "hello", "expected": "HELLO!"},
            {"name": "Empty", "input": "", "expected": "!"},
        ],
        "due_in_days": -2,
    },
]


def make_password(username):
    while True:
        first, second = secrets.SystemRandom().sample(WORDS, 2)
        password = f"{first}-{second}-{secrets.randbelow(90) + 10}"
        try:
            validate_password(password, User(username=username))
            return password
        except Exception:
            continue


class Command(BaseCommand):
    help = "Create (or reset) demo accounts, exercises and progress, and write their logins to a Markdown file."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            default=str(Path(settings.BASE_DIR) / "DEMO_ACCOUNTS.md"),
            help="Where to write the accounts file (default: app/adel_b/DEMO_ACCOUNTS.md, ignored by Git).",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        usernames = [username for username, *_ in ACCOUNTS]
        # Exercises are protected while their professor exists: remove the demo ones first.
        Bug.objects.filter(created_by__username__in=usernames).delete()
        Bug.objects.filter(slug__in=[exercise["slug"] for exercise in EXERCISES]).delete()
        User.objects.filter(username__in=usernames).delete()

        users, passwords = {}, {}
        for username, role, name, _ in ACCOUNTS:
            password = make_password(username)
            email = f"{username}@{DOMAIN}"
            if role == "admin":
                user = User.objects.create_superuser(username, email, password, first_name=name)
            else:
                user = User.objects.create_user(username, email, password, first_name=name)
                user.profile.role = role
                user.profile.save()
            users[username], passwords[username] = user, password

        self.create_progress(users)
        self.write_file(Path(options["output"]), passwords)
        self.stdout.write(self.style.SUCCESS(f"Demo ready: {len(users)} accounts. Logins written to {options['output']}"))

    def create_progress(self, users):
        prof = users["prof_lina"]
        today = timezone.localdate()
        bugs = {}
        for data in EXERCISES:
            fields = {key: value for key, value in data.items() if key not in ("fixed_code", "due_in_days")}
            bug = Bug.objects.create(created_by=prof, **fields)
            bugs[bug.slug] = (bug, data)
            for student in ("student_ali", "student_maria", "student_omar"):
                Assignment.objects.create(
                    bug=bug,
                    student=users[student],
                    assigned_by=prof,
                    due_date=today + datetime.timedelta(days=data["due_in_days"]),
                )

        def attempt(student, slug, passed, days_ago, code=None):
            bug, data = bugs[slug] if slug in bugs else (Bug.objects.get(slug=slug), None)
            row = Attempt.objects.create(
                user=users[student],
                bug=bug,
                code=code or (data["fixed_code"] if passed == len(bug.tests) and data else bug.buggy_code),
                passed_count=passed,
                total_count=len(bug.tests),
            )
            Attempt.objects.filter(pk=row.pk).update(created_at=timezone.now() - datetime.timedelta(days=days_ago))

        zero, word = "demo-forgotten-zero", "demo-shrinking-word"
        # Ali: solved both assignments after a first try, plus catalog practice for a streak.
        attempt("student_ali", zero, 1, 2)
        attempt("student_ali", zero, 3, 1)
        attempt("student_ali", word, 3, 0)
        attempt("student_ali", "remove-negatives", 3, 0)
        for slug in (zero, word):
            Draft.objects.create(user=users["student_ali"], bug=bugs[slug][0], code=bugs[slug][1]["fixed_code"])
        # Maria: editing the zeros exercise, and one wrong submission on the overdue one.
        Draft.objects.create(
            user=users["student_maria"],
            bug=bugs[zero][0],
            code=bugs[zero][1]["buggy_code"].replace("return", "# Why is the first number skipped?\n    return"),
        )
        attempt("student_maria", word, 1, 1)
        # Omar: nothing yet.

    def write_file(self, path, passwords):
        site = settings.DEBUG_GYM_SITE_URL
        rows = "\n".join(
            f"| {self.role_label(role)} | `{username}` | `{username}@{DOMAIN}` | `{passwords[username]}` | {shows} |"
            for username, role, _, shows in ACCOUNTS
        )
        path.write_text(f"""# Debug GYM Demo Accounts

Created {timezone.localtime().strftime('%Y-%m-%d %H:%M')} by `manage.py seed_demo`. Running the
command again deletes these accounts and their data and creates new passwords.

Keep this file private. It is listed in `.gitignore` and must not be committed.

- Website: {site}
- Django admin: {site}/admin/
- Log in with the username or the email.

## Accounts

| Role | Username | Email | Password | What it shows |
|---|---|---|---|---|
{rows}

## Demo Data

Prof. Lina wrote 2 exercises and assigned both to all 3 students:

| Exercise | Due | Ali | Maria | Omar |
|---|---|---|---|---|
| The forgotten zero | in 7 days | Solved (2 submissions) | In progress | Not started |
| The shrinking word | 2 days ago (overdue) | Solved | Not solved (1 / 3) | Not started, overdue |

## Suggested Tour

1. Log in as `prof_lina`: the **Teaching** page lists both exercises with assigned and solved counts.
2. Open **Assign & results** on "The shrinking word" to see each student's status, best score and the overdue mark.
3. Open **Edit** and press **Check with Python** to show that the tests catch the bug.
4. Log in as `student_omar`: **My assignments** shows two open exercises, one overdue.
5. Open one, press **Run Tests**, fix the code, then **Submit**; back as `prof_lina`, the result appears.
6. Log in as `demo_admin` at the Django admin to show how a student is made a professor.
""")

    @staticmethod
    def role_label(role):
        return {"admin": "Admin", Profile.PROFESSOR: "Professor", Profile.STUDENT: "Student"}[role]
