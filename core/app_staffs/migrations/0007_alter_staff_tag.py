# Generated by Django 4.2.7 on 2023-11-16 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tag', '0001_initial'),
        ('app_staffs', '0006_staff_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='tag',
            field=models.ManyToManyField(blank=True, help_text='\n        Выбирите/добавьте уникальный Тег для сотрудника для создание особых групп сотрудников.\n        Добавляйте сотруднику сколько угодно Тегов, включая его в разные группы.\n        ', to='app_tag.tags', verbose_name='ТЕГ'),
        ),
    ]
