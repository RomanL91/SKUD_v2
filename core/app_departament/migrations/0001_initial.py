# Generated by Django 4.2.7 on 2023-11-17 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Departament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_departament', models.CharField(max_length=200, unique=True, verbose_name='Департамент')),
                ('desc_dep', models.TextField(blank=True, verbose_name='Описание')),
                ('interception', models.BooleanField(default=False, help_text='Ограничит доступ на всех проходных/контроллерах сотрудников<br>\n        принадлежащие к данному Департаменту', verbose_name='Перехват')),
            ],
            options={
                'verbose_name': 'Департамент',
                'verbose_name_plural': 'Департаменты',
            },
        ),
    ]