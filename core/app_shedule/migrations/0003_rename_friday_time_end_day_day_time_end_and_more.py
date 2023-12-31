# Generated by Django 4.2.7 on 2023-11-21 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_shedule', '0002_alter_day_options_alter_schedule_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='day',
            old_name='friday_time_end',
            new_name='day_time_end',
        ),
        migrations.RenameField(
            model_name='day',
            old_name='friday_time_start',
            new_name='day_time_start',
        ),
        migrations.RemoveField(
            model_name='day',
            name='monday_time_end',
        ),
        migrations.RemoveField(
            model_name='day',
            name='monday_time_start',
        ),
        migrations.RemoveField(
            model_name='day',
            name='saturday_time_end',
        ),
        migrations.RemoveField(
            model_name='day',
            name='saturday_time_start',
        ),
        migrations.RemoveField(
            model_name='day',
            name='sunday_time_end',
        ),
        migrations.RemoveField(
            model_name='day',
            name='sunday_time_start',
        ),
        migrations.RemoveField(
            model_name='day',
            name='thursday_time_end',
        ),
        migrations.RemoveField(
            model_name='day',
            name='thursday_time_start',
        ),
        migrations.RemoveField(
            model_name='day',
            name='tuesday_time_end',
        ),
        migrations.RemoveField(
            model_name='day',
            name='tuesday_time_start',
        ),
        migrations.RemoveField(
            model_name='day',
            name='wednesday_time_end',
        ),
        migrations.RemoveField(
            model_name='day',
            name='wednesday_time_start',
        ),
        migrations.AlterField(
            model_name='day',
            name='week_day',
            field=models.CharField(default=0, max_length=20, verbose_name='День недели'),
        ),
    ]
