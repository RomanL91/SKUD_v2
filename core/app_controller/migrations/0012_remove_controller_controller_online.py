# Generated by Django 4.2.7 on 2023-12-26 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_controller', '0011_alter_controller_direction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='controller',
            name='controller_online',
        ),
    ]