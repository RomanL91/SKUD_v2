# Generated by Django 4.2.7 on 2023-11-17 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_departament', '0001_initial'),
        ('app_staffs', '0010_alter_staff_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='departament',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_departament.departament', verbose_name='Департамент'),
        ),
    ]
