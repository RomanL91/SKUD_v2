# Generated by Django 4.2.7 on 2023-11-15 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_staffs', '0003_alter_staff_patromic'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, upload_to='staff_photo/', verbose_name='Фотография')),
                ('desc', models.TextField(blank=True, max_length=1500, verbose_name='Описание')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_staffs.staff', verbose_name='Сотрудник')),
            ],
            options={
                'verbose_name': 'Фотография',
                'verbose_name_plural': 'Фотографии',
            },
        ),
    ]
