# Generated by Django 4.2.7 on 2023-11-27 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_shedule', '0007_remove_schedule_strict_schedule_and_more'),
        ('app_checkpoint', '0003_checkpoint_checkpoint_block'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkpoint',
            name='checpoint_schedule',
            field=models.ForeignKey(blank=True, help_text='\n        Выбирите расписание для работы проходной.<br>\n        Полезно, когда есть проходные, где не должно происходить каких-либо<br>\n        действий согласно расписанию, напрмер, такие проходные, где после 12:00<br>\n        не должно происходить никаких действий, а если такие будут,<br> \n        то пост получит об уведомление.\n        ', null=True, on_delete=django.db.models.deletion.CASCADE, to='app_shedule.schedule', verbose_name='Расписание проходной'),
        ),
    ]
