# Generated by Django 4.2.7 on 2023-11-24 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_event', '0002_alter_event_event_card_dec_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_reason_granted',
            field=models.CharField(blank=True, default='тип не определен', max_length=200, null=True, verbose_name='Тип решения по доступу'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_granted',
            field=models.BooleanField(default=False, verbose_name='Решение по доступу для события'),
        ),
    ]
