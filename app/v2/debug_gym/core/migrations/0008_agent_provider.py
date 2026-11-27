# [Backend Dev] Preserve existing platform routing while adding personal provider choice

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_teaching_customer_feedback"),
    ]

    operations = [
        migrations.AddField(
            model_name="agentcredential",
            name="provider",
            field=models.CharField(
                choices=[
                    ("platform", "Platform provider"),
                    ("openai", "OpenAI"),
                    ("openrouter", "OpenRouter"),
                ],
                default="platform",
                max_length=20,
            ),
        ),
    ]
