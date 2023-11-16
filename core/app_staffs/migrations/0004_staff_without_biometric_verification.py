# Generated by Django 4.2.7 on 2023-11-16 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_staffs', '0003_alter_staff_patromic'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='without_biometric_verification',
            field=models.BooleanField(blank=True, default=False, editable=False, help_text='Обладатель сможет проходить через проходные без проверки биометрии\n                        на проходных где она используется', verbose_name='Открыть доступ без проверки биометрии'),
        ),
    ]