# Kept as a no-op on purpose.
#
# Two pull requests (#184 and #186) both added Submission.tests_passed and
# Submission.tests_total. #186's migration (0002_bug_compose_config_bug_project_files_and_more)
# adds them with the constraint the model uses (submission_valid_test_counts), so this
# migration must not add them a second time. Its name stays so databases that recorded
# it keep a valid history; 0005_merge joins the two branches of the graph.
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = []
