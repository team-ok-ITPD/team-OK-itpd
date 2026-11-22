# [Backend Dev] Separate group number while preserving existing group names/data
from django.db import migrations, models
from django.db.models.functions import Lower


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_merge_bug_tests_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="studygroup",
            name="group_number",
            field=models.CharField(blank=True, default="", max_length=50),
        ),
        migrations.AddConstraint(
            model_name="studygroup",
            constraint=models.UniqueConstraint(
                Lower("name"), Lower("group_number"),
                condition=~models.Q(group_number=""),
                name="unique_course_group_number",
            ),
        ),
    ]
