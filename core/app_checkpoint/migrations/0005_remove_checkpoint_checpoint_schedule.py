# Generated by Django 4.2.7 on 2023-11-27 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_checkpoint', '0004_checkpoint_checpoint_schedule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkpoint',
            name='checpoint_schedule',
        ),
    ]
