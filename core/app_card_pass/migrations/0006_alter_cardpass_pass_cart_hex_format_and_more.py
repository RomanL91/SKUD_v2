# Generated by Django 4.2.7 on 2023-11-14 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_staffs', '0003_alter_staff_patromic'),
        ('app_card_pass', '0005_alter_cardpass_activate_card_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardpass',
            name='pass_cart_hex_format',
            field=models.CharField(blank=True, editable=False, max_length=10, verbose_name='Номер пропуска в HEX формате'),
        ),
        migrations.AlterField(
            model_name='cardpass',
            name='staff',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app_staffs.staff', verbose_name='Сотрудник'),
        ),
    ]
