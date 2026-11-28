# [Shared] Preserve group history while allowing administrator deactivation.
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("core", "0012_merge_20261127_2037")]

    operations = [
        migrations.AddField(
            model_name="studygroup",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
