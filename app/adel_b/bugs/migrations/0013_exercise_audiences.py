from django.db import migrations, models


def classify_existing_exercises(apps, schema_editor):
    Assignment = apps.get_model("bugs", "Assignment")
    Bug = apps.get_model("bugs", "Bug")
    Bug.objects.filter(created_by__isnull=True).update(audience="public")
    Bug.objects.filter(created_by__isnull=False, id__in=Assignment.objects.values("bug_id")).update(audience="group")


class Migration(migrations.Migration):
    dependencies = [("bugs", "0012_group_assignments")]

    operations = [
        migrations.AddField(
            model_name="bug",
            name="audience",
            field=models.CharField(
                choices=[("private", "Private"), ("public", "Public"), ("group", "Group")],
                default="private",
                max_length=10,
            ),
        ),
        migrations.RunPython(classify_existing_exercises, migrations.RunPython.noop),
    ]
