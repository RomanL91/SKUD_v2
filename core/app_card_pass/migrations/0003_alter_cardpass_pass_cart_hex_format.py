# Generated by Django 4.2.7 on 2023-11-14 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_card_pass', '0002_alter_cardpass_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardpass',
            name='pass_cart_hex_format',
            field=models.CharField(max_length=10, verbose_name='Номер пропуска в HEX формате'),
        ),
    ]
