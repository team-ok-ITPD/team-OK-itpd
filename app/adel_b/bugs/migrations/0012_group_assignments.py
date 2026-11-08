import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def migrate_individual_assignments(apps, schema_editor):
    Assignment = apps.get_model("bugs", "Assignment")
    GroupMembership = apps.get_model("bugs", "GroupMembership")
    TeachingGroup = apps.get_model("bugs", "TeachingGroup")

    for assignment in Assignment.objects.select_related("student", "assigned_by", "bug__created_by"):
        if assignment.assigned_by and assignment.bug.created_by and assignment.assigned_by_id != assignment.bug.created_by_id:
            raise RuntimeError(f"Assignment {assignment.pk} has conflicting teacher ownership.")
        teacher = assignment.bug.created_by or assignment.assigned_by
        if teacher is None:
            raise RuntimeError(f"Assignment {assignment.pk} has no teacher to own its migrated group.")
        suffix = f" ({assignment.student_id})"
        name = f"Migrated - {assignment.student.username}"[:150 - len(suffix)] + suffix
        group, _ = TeachingGroup.objects.get_or_create(teacher=teacher, name=name)
        GroupMembership.objects.get_or_create(group=group, student=assignment.student)
        assignment.group = group
        assignment.save(update_fields=["group"])


class Migration(migrations.Migration):
    dependencies = [
        ("bugs", "0011_protect_exercise_owner"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TeachingGroup",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                ("teacher", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="teaching_groups", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["name", "id"]},
        ),
        migrations.CreateModel(
            name="GroupMembership",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("group", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="memberships", to="bugs.teachinggroup")),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="group_memberships", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["student__username", "id"]},
        ),
        migrations.AddField(
            model_name="teachinggroup",
            name="students",
            field=models.ManyToManyField(related_name="learning_groups", through="bugs.GroupMembership", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(model_name="teachinggroup", constraint=models.UniqueConstraint(fields=("teacher", "name"), name="unique_group_name_per_teacher")),
        migrations.AddConstraint(model_name="groupmembership", constraint=models.UniqueConstraint(fields=("group", "student"), name="one_membership_per_group_student")),
        migrations.AddField(
            model_name="assignment",
            name="group",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name="assignments", to="bugs.teachinggroup"),
        ),
        migrations.RunPython(migrate_individual_assignments, migrations.RunPython.noop),
        migrations.RemoveConstraint(model_name="assignment", name="one_assignment_per_student_and_bug"),
        migrations.RemoveField(model_name="assignment", name="student"),
        migrations.RemoveField(model_name="assignment", name="assigned_by"),
        migrations.RenameField(model_name="assignment", old_name="due_date", new_name="deadline"),
        migrations.AlterModelOptions(name="assignment", options={"ordering": ["deadline", "created_at"]}),
        migrations.AlterField(model_name="assignment", name="group", field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="assignments", to="bugs.teachinggroup")),
        migrations.AddConstraint(model_name="assignment", constraint=models.UniqueConstraint(fields=("bug", "group"), name="one_assignment_per_group_and_bug")),
        migrations.RemoveField(model_name="bug", name="duration"),
    ]
