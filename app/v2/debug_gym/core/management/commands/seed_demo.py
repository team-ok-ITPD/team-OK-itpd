# [Backend Dev] Fill the database with demo users, groups, bugs, assignments and submissions
"""Demo data for local development and demos.

    python manage.py seed_demo            # add the demo data (once)
    python manage.py seed_demo --reset    # delete the demo data and add it again
    python manage.py seed_demo --delete   # delete the demo data only

Every demo account uses an email ending in @demo.debuggym.test, and --reset /
--delete only ever touch data that belongs to those accounts. Real accounts and
their data are never changed.
"""
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from core.models import Assignment, Bug, StudyGroup, Submission, User

DOMAIN = "@demo.debuggym.test"
DEFAULT_PASSWORD = "demo-pass-123"  # demo accounts only; never use for real users

ADMINS = [("admin", "Amina Admin")]
PROFESSORS = [("prof.karim", "Karim Benali"), ("prof.sara", "Sara Haddad")]
STUDENTS = [
    ("ali", "Ali Mansour"), ("lina", "Lina Cherif"), ("omar", "Omar Saadi"),
    ("yasmine", "Yasmine Rahal"), ("nour", "Nour Belkacem"), ("adam", "Adam Ferhat"),
    ("ines", "Ines Toumi"), ("rayan", "Rayan Djebbar"),
]
GROUPS = [
    # name, professor, description, students
    ("Python A", "prof.karim", "First-year Python, morning group.", ["ali", "lina", "omar", "yasmine"]),
    ("Python B", "prof.karim", "First-year Python, afternoon group.", ["nour", "adam", "ines", "ali"]),
    ("Mobile Dev", "prof.sara", "Dart and Flutter basics.", ["rayan", "lina", "nour"]),
]

# Exercise metadata, buggy source and sample student submission
BUGS = [
    (
        "Sum skips the last item", "python", "easy", "public", "prof.karim",
        "total() should add every number in the list, but the result is always too small.",
        "def total(numbers):\n    s = 0\n    for i in range(len(numbers) - 1):\n        s += numbers[i]\n    return s\n",
        "def total(numbers):\n    s = 0\n    for i in range(len(numbers)):\n        s += numbers[i]\n    return s\n",
    ),
    (
        "Adult check is off by one", "python", "easy", "public", "prof.karim",
        "is_adult(18) should be True, but it returns False.",
        "def is_adult(age):\n    return age > 18\n",
        "def is_adult(age):\n    return age >= 18\n",
    ),
    (
        "Average of an empty list crashes", "python", "medium", "public", "prof.sara",
        "average([]) should return 0, but it raises ZeroDivisionError.",
        "def average(xs):\n    return sum(xs) / len(xs)\n",
        "def average(xs):\n    if not xs:\n        return 0\n    return sum(xs) / len(xs)\n",
    ),
    (
        "Shared default list", "python", "hard", "public", "prof.karim",
        "Each call to add_tag() should start with a fresh list, but tags from earlier calls keep appearing.",
        "def add_tag(tag, tags=[]):\n    tags.append(tag)\n    return tags\n",
        "def add_tag(tag, tags=None):\n    if tags is None:\n        tags = []\n    tags.append(tag)\n    return tags\n",
    ),
    (
        "Counting vowels misses capitals", "python", "easy", "private", "prof.karim",
        'count_vowels("Apple") should return 2, but it returns 1.',
        'def count_vowels(word):\n    return sum(1 for ch in word if ch in "aeiou")\n',
        'def count_vowels(word):\n    return sum(1 for ch in word.lower() if ch in "aeiou")\n',
    ),
    (
        "Second largest returns the largest", "python", "medium", "private", "prof.karim",
        "second_largest([3, 9, 5]) should return 5, but it returns 9.",
        "def second_largest(xs):\n    ordered = sorted(xs)\n    return ordered[-1]\n",
        "def second_largest(xs):\n    ordered = sorted(set(xs))\n    return ordered[-2]\n",
    ),
    (
        "Null string length", "dart", "medium", "private", "prof.sara",
        "lengthOf(null) should return 0, but the app crashes with a null error.",
        "int lengthOf(String? s) {\n  return s!.length;\n}\n",
        "int lengthOf(String? s) {\n  return s?.length ?? 0;\n}\n",
    ),
    (
        "Counter never updates", "dart", "hard", "public", "prof.sara",
        "Tapping the button should show the new count, but the number on screen never changes.",
        "void increment() {\n  count++;\n}\n",
        "void increment() {\n  setState(() {\n    count++;\n  });\n}\n",
    ),
    (
        "Loose equality surprise", "javascript", "easy", "public", "prof.sara",
        'isZero("") should be false, but it returns true.',
        "function isZero(x) {\n  return x == 0;\n}\n",
        "function isZero(x) {\n  return x === 0;\n}\n",
    ),
    # Bugs students made for their own practice (with AI or by editing)
    (
        "Palindrome ignores case", "python", "easy", "private", "lina",
        'is_palindrome("Level") should be True, but it returns False.',
        "def is_palindrome(word):\n    return word == word[::-1]\n",
        "def is_palindrome(word):\n    word = word.lower()\n    return word == word[::-1]\n",
    ),
    (
        "FizzBuzz order", "python", "medium", "public", "ali",
        "fizzbuzz(15) should return 'FizzBuzz', but it returns 'Fizz'.",
        'def fizzbuzz(n):\n    if n % 3 == 0:\n        return "Fizz"\n    if n % 5 == 0:\n        return "Buzz"\n    if n % 15 == 0:\n        return "FizzBuzz"\n    return str(n)\n',
        'def fizzbuzz(n):\n    if n % 15 == 0:\n        return "FizzBuzz"\n    if n % 3 == 0:\n        return "Fizz"\n    if n % 5 == 0:\n        return "Buzz"\n    return str(n)\n',
    ),
]

# pytest files for the Python bugs; the code is saved as main.py in VS Code.
TESTS = {
    "Sum skips the last item": (
        "from main import *\n\n\n"
        "def test_adds_every_number():\n    assert total([1, 2, 3]) == 6\n\n\n"
        "def test_single_number():\n    assert total([5]) == 5\n\n\n"
        "def test_empty_list():\n    assert total([]) == 0\n"
    ),
    "Adult check is off by one": (
        "from main import *\n\n\n"
        "def test_eighteen_is_adult():\n    assert is_adult(18) is True\n\n\n"
        "def test_seventeen_is_not():\n    assert is_adult(17) is False\n\n\n"
        "def test_thirty_is_adult():\n    assert is_adult(30) is True\n"
    ),
    "Average of an empty list crashes": (
        "from main import *\n\n\n"
        "def test_empty_list_is_zero():\n    assert average([]) == 0\n\n\n"
        "def test_normal_average():\n    assert average([2, 4]) == 3\n"
    ),
    "Shared default list": (
        "from main import *\n\n\n"
        "def test_each_call_starts_fresh():\n    add_tag(\"a\")\n    assert add_tag(\"b\") == [\"b\"]\n\n\n"
        "def test_given_list_is_used():\n    assert add_tag(\"b\", [\"a\"]) == [\"a\", \"b\"]\n"
    ),
    "Counting vowels misses capitals": (
        "from main import *\n\n\n"
        "def test_capital_vowel():\n    assert count_vowels(\"Apple\") == 2\n\n\n"
        "def test_all_capitals():\n    assert count_vowels(\"AEIOU\") == 5\n\n\n"
        "def test_no_vowels():\n    assert count_vowels(\"xyz\") == 0\n"
    ),
    "Second largest returns the largest": (
        "from main import *\n\n\n"
        "def test_second_largest():\n    assert second_largest([3, 9, 5]) == 5\n\n\n"
        "def test_with_duplicates():\n    assert second_largest([9, 9, 4]) == 4\n"
    ),
    "Palindrome ignores case": (
        "from main import *\n\n\n"
        "def test_mixed_case():\n    assert is_palindrome(\"Level\") is True\n\n\n"
        "def test_not_palindrome():\n    assert is_palindrome(\"debug\") is False\n"
    ),
    "FizzBuzz order": (
        "from main import *\n\n\n"
        "def test_fifteen():\n    assert fizzbuzz(15) == \"FizzBuzz\"\n\n\n"
        "def test_three():\n    assert fizzbuzz(3) == \"Fizz\"\n\n\n"
        "def test_five():\n    assert fizzbuzz(5) == \"Buzz\"\n\n\n"
        "def test_plain():\n    assert fizzbuzz(7) == \"7\"\n"
    ),
}

# title, bug title, professor, groups, deadline in days (negative = past), status, instructions
ASSIGNMENTS = [
    ("Week 1: loops", "Sum skips the last item", "prof.karim", ["Python A", "Python B"], -10, "active",
     "Fix total() so it adds every number. Do not change the function name."),
    ("Week 2: conditions", "Adult check is off by one", "prof.karim", ["Python A"], -3, "active",
     "Read the description carefully and fix the comparison."),
    ("Week 3: strings", "Counting vowels misses capitals", "prof.karim", ["Python A", "Python B"], 1, "active",
     "Make count_vowels work for upper-case letters too."),
    ("Week 4: lists", "Second largest returns the largest", "prof.karim", ["Python A"], 6, "active",
     "Think about duplicates as well."),
    ("Old quiz (closed)", "Shared default list", "prof.karim", ["Python B"], 5, "closed",
     "This quiz was closed early by the professor."),
    ("Null safety basics", "Null string length", "prof.sara", ["Mobile Dev"], 3, "active",
     "Use Dart null-safety operators instead of the ! operator."),
]

# student, assignment title (or None for practice), bug title for practice, fixed?, status, grade, feedback, days ago
SUBMISSIONS = [
    ("ali", "Week 1: loops", None, True, "graded", "9.5", "Clean fix. Nice that you kept the name.", 9),
    ("lina", "Week 1: loops", None, True, "graded", "8", "Correct, but you also changed the variable names.", 9),
    ("omar", "Week 1: loops", None, False, "graded", "5.5", "The loop still skips the last item.", 8),
    ("nour", "Week 1: loops", None, True, "graded", "10", "Perfect.", 8),
    ("adam", "Week 1: loops", None, True, "submitted", None, "", 7),
    ("ali", "Week 2: conditions", None, True, "graded", "10", "Exactly right.", 3),
    ("lina", "Week 2: conditions", None, True, "submitted", None, "", 4),
    ("yasmine", "Week 3: strings", None, True, "submitted", None, "", 0),
    ("ali", "Week 3: strings", None, True, "submitted", None, "", 0),
    ("rayan", "Null safety basics", None, True, "submitted", None, "", 1),
    ("ali", None, "Average of an empty list crashes", False, "submitted", None, "", 2),
    ("ali", None, "Average of an empty list crashes", True, "submitted", None, "", 1),
    ("lina", None, "Loose equality surprise", True, "submitted", None, "", 2),
    ("nour", None, "FizzBuzz order", True, "submitted", None, "", 1),
]


def email(handle):
    return f"{handle}{DOMAIN}"


class Command(BaseCommand):
    help = "Add demo users, groups, bugs, assignments and submissions (emails end in @demo.debuggym.test)."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Delete the demo data first, then add it again.")
        parser.add_argument("--delete", action="store_true", help="Only delete the demo data.")
        parser.add_argument("--password", default=DEFAULT_PASSWORD, help="Password for every demo account.")

    def handle(self, *args, password, reset, delete, **options):
        if reset or delete:
            self.delete_demo()
            if delete:
                return
        elif User.objects.filter(email__endswith=DOMAIN).exists():
            raise CommandError("Demo data already exists. Use --reset to recreate it or --delete to remove it.")
        with transaction.atomic():
            self.create_demo(password)
        self.print_summary(password)

    def delete_demo(self):
        demo_users = User.objects.filter(email__endswith=DOMAIN)
        with transaction.atomic():
            # Order matters: assignments protect their bug and professor.
            Assignment.objects.filter(professor__in=demo_users).delete()
            Submission.objects.filter(student__in=demo_users).delete()
            Bug.objects.filter(created_by__in=demo_users).delete()
            StudyGroup.objects.filter(professor__in=demo_users).delete()
            count, _ = demo_users.delete()
        self.stdout.write(f"Deleted the demo data ({count} demo-owned rows).")

    def create_demo(self, password):
        now = timezone.now()
        users = {}
        for role, people in ((User.Role.ADMIN, ADMINS), (User.Role.PROFESSOR, PROFESSORS),
                             (User.Role.STUDENT, STUDENTS)):
            for handle, name in people:
                users[handle] = User.objects.create_user(email(handle), name, password, role=role)

        groups = {}
        for name, prof, description, members in GROUPS:
            group = StudyGroup.objects.create(name=name, description=description, professor=users[prof])
            group.students.add(*(users[m] for m in members))
            groups[name] = group

        bugs = {}
        sample_submissions = {}
        for title, language, difficulty, visibility, author, description, buggy, solution in BUGS:
            sample_submissions[title] = solution
            bugs[title] = Bug.objects.create(
                title=title, language=language, difficulty=difficulty, visibility=visibility,
                created_by=users[author], description=description,
                buggy_code=buggy, tests_code=TESTS.get(title, ""),
            )

        assignments = {}
        for title, bug, prof, group_names, days, status, instructions in ASSIGNMENTS:
            assignments[title] = []
            for group_name in group_names:
                assignment = Assignment.objects.create(
                    title=title, bug=bugs[bug], professor=users[prof], status=status,
                    deadline=now + timedelta(days=days), instructions=instructions,
                )
                assignment.groups.add(groups[group_name])
                assignments[title].append(assignment)

        for handle, assignment_title, practice_bug, fixed, status, grade, feedback, days_ago in SUBMISSIONS:
            candidates = assignments[assignment_title] if assignment_title else []
            assignment = next((row for row in candidates if row.groups.filter(students=users[handle]).exists()),
                              candidates[0] if candidates else None)
            bug = assignment.bug if assignment else bugs[practice_bug]
            submission = Submission.objects.create(
                student=users[handle], bug=bug, assignment=assignment,
                # Correct work submits the real fix; wrong work is still the buggy code.
                submitted_code=sample_submissions[bug.title] if fixed else bug.buggy_code,
                status=status, grade=Decimal(grade) if grade else None, feedback=feedback,
                graded_at=now - timedelta(days=max(days_ago - 1, 0)) if status == "graded" else None,
            )
            # submitted_at is set automatically; move it back so the history looks realistic.
            Submission.objects.filter(pk=submission.pk).update(submitted_at=now - timedelta(days=days_ago))

    def print_summary(self, password):
        self.stdout.write(self.style.SUCCESS("Demo data added."))
        self.stdout.write(
            f"  {User.objects.filter(email__endswith=DOMAIN).count()} users, "
            f"{StudyGroup.objects.filter(professor__email__endswith=DOMAIN).count()} groups, "
            f"{Bug.objects.filter(created_by__email__endswith=DOMAIN).count()} bugs, "
            f"{Assignment.objects.filter(professor__email__endswith=DOMAIN).count()} assignments, "
            f"{Submission.objects.filter(student__email__endswith=DOMAIN).count()} submissions"
        )
        self.stdout.write(f"\nEvery demo account uses the password: {password}")
        for label, people in (("Admin", ADMINS), ("Professors", PROFESSORS), ("Students", STUDENTS)):
            self.stdout.write(f"  {label}: " + ", ".join(email(handle) for handle, _ in people))
        self.stdout.write(f"\nTry {email('ali')}: this account has every assignment status, grades and practice attempts.")

