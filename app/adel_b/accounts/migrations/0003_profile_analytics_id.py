import uuid

from django.db import migrations, models


def give_each_profile_an_id(apps, schema_editor):
    """Existing profiles get their own random analytics identifier."""
    Profile = apps.get_model("accounts", "Profile")
    for profile in Profile.objects.all():
        profile.analytics_id = uuid.uuid4()
        profile.save(update_fields=["analytics_id"])


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_existing_users_are_students"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="analytics_id",
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.RunPython(give_each_profile_an_id, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="profile",
            name="analytics_id",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
