# Generated by Django 4.2.7 on 2023-11-21 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_position', '0002_alter_position_options_alter_position_tag'),
        ('app_shedule', '0006_alter_day_break_in_schedule_end_and_more'),
        ('app_staffs', '0012_staff_access_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_shedule.schedule', verbose_name='Расписание сотрудника'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_position.position', verbose_name='Должость'),
        ),
    ]
