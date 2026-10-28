from django.db import migrations

BUGGY_CODE = '''def remove_negatives(numbers: list[int]) -> list[int]:
    """Return the input list without negative numbers."""
    for number in numbers:
        if number < 0:
            numbers.remove(number)
    return numbers
'''


def seed_first_bug(apps, schema_editor):
    Bug = apps.get_model("bugs", "Bug")
    Bug.objects.get_or_create(
        slug="remove-negatives",
        defaults={
            "title": "The surviving negative",
            "language": "Python 3",
            "difficulty": "Easy",
            "duration": "10-15 min",
            "topic": "Lists and loops",
            "description": (
                "A filter should remove every negative number from a list, but some "
                "negative values survive. Reproduce the failure and find out why."
            ),
            "buggy_code": BUGGY_CODE,
        },
    )


def unseed_first_bug(apps, schema_editor):
    apps.get_model("bugs", "Bug").objects.filter(slug="remove-negatives").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("bugs", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_first_bug, unseed_first_bug),
    ]
