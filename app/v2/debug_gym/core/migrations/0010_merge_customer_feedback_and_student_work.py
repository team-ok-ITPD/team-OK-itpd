# [Backend Dev] Join the student VS Code work (PR #196) with PR #201, and keep tests_code.
#
# 0007_merge_group_number_and_project_tests moved Bug.tests_code into
# Bug.project_files (test_main.py) and removed the column. PR #201
# (0007_teaching_customer_feedback .. 0009_exercise_dockerfile) still uses
# Bug.tests_code in the professor pages, so it is added back here, empty.
# Existing tests were already copied into project_files and are not lost.
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_merge_group_number_and_project_tests"),
        ("core", "0009_exercise_dockerfile"),
    ]

    operations = [
        migrations.AddField(
            model_name="bug",
            name="tests_code",
            field=models.TextField(
                blank=True,
                default="",
                help_text="Optional pytest file for Python bugs. The code is saved as main.py, "
                "so tests start with: from main import *",
            ),
        ),
    ]
