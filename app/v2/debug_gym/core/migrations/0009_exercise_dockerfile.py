# [Backend Dev] Store optional Dockerfiles without reinterpreting legacy Compose data

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_agent_provider"),
    ]

    operations = [
        migrations.AddField(
            model_name="bug",
            name="dockerfile_config",
            field=models.TextField(blank=True),
        ),
    ]
