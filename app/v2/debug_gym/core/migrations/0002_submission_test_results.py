from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='tests_passed',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='submission',
            name='tests_total',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddConstraint(
            model_name='submission',
            constraint=models.CheckConstraint(
                condition=models.Q(
                    models.Q(('tests_passed__isnull', True), ('tests_total__isnull', True)),
                    models.Q(
                        ('tests_passed__isnull', False),
                        ('tests_passed__lte', models.F('tests_total')),
                        ('tests_total__isnull', False),
                    ),
                    _connector='OR',
                ),
                name='submission_test_counts_consistent',
            ),
        ),
    ]
