# Generated by Django 5.2.3 on 2025-06-14 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_user_target_weekly_hours_alter_user_weekly_hours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='weekly_hours',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Number of hours the user worked per week.', max_digits=4),
        ),
    ]
