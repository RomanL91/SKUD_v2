# Generated by Django 4.2.7 on 2023-11-15 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_card_pass', '0009_alter_cardpass_pass_cart_hex_format'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardpass',
            name='pass_cart_hex_format',
            field=models.CharField(max_length=12, unique=True, verbose_name='Номер пропуска в HEX формате'),
        ),
    ]
