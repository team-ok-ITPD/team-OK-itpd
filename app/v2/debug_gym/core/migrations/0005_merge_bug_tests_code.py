# [Backend Dev] Join independent exercise-test and teaching-workflow migrations
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_bug_tests_code"),
        ("core", "0004_assignmentreview"),
    ]

    operations = []
