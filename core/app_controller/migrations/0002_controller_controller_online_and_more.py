# Generated by Django 4.2.7 on 2023-11-20 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_controller', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='controller',
            name='controller_online',
            field=models.CharField(default='0', max_length=10, verbose_name='Режимы контроллера'),
        ),
        migrations.AlterField(
            model_name='controller',
            name='controller_activity',
            field=models.CharField(default='0', help_text='\n        Выбирите состояние контроллера и сохраните его <br>\n        для включения или выключения.\n        ', max_length=10, verbose_name='Состояние контроллера'),
        ),
    ]
