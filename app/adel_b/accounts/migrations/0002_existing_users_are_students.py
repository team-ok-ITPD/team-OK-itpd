from django.conf import settings
from django.db import migrations


def give_existing_users_a_profile(apps, schema_editor):
    """Accounts made before roles existed become students."""
    User = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    Profile = apps.get_model("accounts", "Profile")
    for user in User.objects.filter(profile__isnull=True):
        Profile.objects.create(user=user, role="student")


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_profile"),
    ]

    operations = [
        migrations.RunPython(give_existing_users_a_profile, migrations.RunPython.noop),
    ]
