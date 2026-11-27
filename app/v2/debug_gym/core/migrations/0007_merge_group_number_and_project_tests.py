# [Backend Dev] Join two migrations made in parallel; no database changes.
#
# 0006_studygroup_group_number (PR #197, administrator feedback) and
# 0006_move_tests_into_project_files (PR #196, student VS Code work) both follow
# 0005_merge_bug_tests_code. This empty migration makes them one history again.
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_move_tests_into_project_files"),
        ("core", "0006_studygroup_group_number"),
    ]

    operations = []
