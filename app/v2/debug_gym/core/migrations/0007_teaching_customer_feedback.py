# [Backend Dev] Customer feedback: independent assignments, courses and no reference solution

from django.db import migrations, models


def separate_groups(apps, schema_editor):
    Group = apps.get_model("core", "StudyGroup")
    Assignment = apps.get_model("core", "Assignment")
    Submission = apps.get_model("core", "Submission")
    Review = apps.get_model("core", "AssignmentReview")
    alias = schema_editor.connection.alias
    for group in Group.objects.using(alias).all():
        group.course = group.name
        group.save(using=alias, update_fields=["course"])
    for assignment in Assignment.objects.using(alias).all():
        groups = list(assignment.groups.using(alias).order_by("pk"))
        for group in groups[1:]:
            clone = Assignment.objects.using(alias).create(
                title=assignment.title, instructions=assignment.instructions,
                bug_id=assignment.bug_id, professor_id=assignment.professor_id,
                deadline=assignment.deadline, status=assignment.status,
            )
            clone.groups.add(group)
            Assignment.objects.using(alias).filter(pk=clone.pk).update(created_at=assignment.created_at)
            members = group.students.using(alias).values_list("pk", flat=True)
            for attempt in Submission.objects.using(alias).filter(assignment=assignment, student_id__in=members):
                values = {f.attname: getattr(attempt, f.attname) for f in Submission._meta.concrete_fields
                          if not f.primary_key and f.name != "assignment"}
                copied = Submission.objects.using(alias).create(assignment=clone, **values)
                Submission.objects.using(alias).filter(pk=copied.pk).update(submitted_at=attempt.submitted_at)
            review = Review.objects.using(alias).filter(assignment=assignment).first()
            if review:
                Review.objects.using(alias).create(
                    assignment=clone, status=review.status, detail=review.detail,
                    finished_at=review.finished_at,
                )
        if groups:
            assignment.groups.set(groups[:1])
    # Keep one current assignment per exercise/group; preserve older duplicates as history.
    current = set()
    for assignment in Assignment.objects.using(alias).order_by("-created_at", "-pk"):
        group_id = assignment.groups.values_list("pk", flat=True).first()
        if group_id is None:
            continue
        key = (assignment.professor_id, assignment.bug_id, group_id)
        if key in current:
            assignment.is_withdrawn = True
            assignment.status = "closed"
            assignment.save(using=alias, update_fields=["is_withdrawn", "status"])
        else:
            current.add(key)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_studygroup_group_number"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bug",
            name="solution_code",
        ),
        migrations.AddField(
            model_name="assignment",
            name="is_withdrawn",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="studygroup",
            name="course",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name="bug",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="bug",
            name="difficulty",
            field=models.CharField(
                blank=True,
                choices=[("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")],
                default="easy",
                max_length=10,
            ),
        ),
        migrations.RunPython(separate_groups, migrations.RunPython.noop),
    ]
