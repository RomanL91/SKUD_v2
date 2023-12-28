import re

from django.db import models
from django.db.models.signals import post_save, post_delete, pre_save

from django.dispatch import receiver

from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _

from app_staffs.models import Staff


def pass_card_dec_format_valid(value):
    if len(value) == 10:
        try:
            pass_number = re.match("^([0-9]{10})$", value).group(0)
        except:
            raise ValidationError(
                _("%(value)s не верный формат! Ожидалось ХХХХХХХХХХ (например: 0007339662)"),
                params={"value": value},
            )
    elif len(value) == 9:
        try:
            pass_number = re.match("^([0-9]{3})([\D])([0-9]{5})$", value)
            part_1_pass_number = pass_number.group(1)
            part_3_pass_number = pass_number.group(3)
        except:
            raise ValidationError(
                _("%(value)s не верный формат! Ожидалось ХХХ.ХХХХХ (например: 111.65166)"),
                params={"value": value},
            )
    else:
        raise ValidationError(
                _("%(value)s не верный формат! Форматы: ХХХХХХХХХХ (например: 0007339662),\nХХХ.ХХХХХ (например: 111.65166)"),
                params={"value": value},
            )
    

class CardPass(models.Model):
    pass_card_dec_format = models.CharField(
        validators=[pass_card_dec_format_valid,],
        verbose_name='Номер пропуска в DEC формате', max_length=10, unique=True
    )
    pass_cart_hex_format = models.CharField(
        verbose_name='Номер пропуска в HEX формате', max_length=12, unique=False,
        editable=False
    )
    activate_card = models.BooleanField(
        verbose_name='Активировать карту', default=True, 
        help_text='Отключите, если не хотите, чтобы сотрудник использовал данную карту'
    )
    staff = models.ForeignKey(
        Staff, on_delete=models.CASCADE, verbose_name='Сотрудник',
    )


    class Meta:
        verbose_name = 'Карта/Пропуск'
        verbose_name_plural = 'Карты/Пропуски'


    @property
    def formatting_in_hex(self): # под рефактор
        mask = ['000000']
        match self.pass_card_dec_format:
            case num if len(num) == 10:
                    pass_number = re.match("^([0-9]{10})$", num).group(0)
                    hex_n = hex(int(pass_number))[2:]
                    mask.append(hex_n)
                    hex_pass_number = ''.join(mask).upper()
            case num if len(num) == 9:
                    pass_number = re.match("^([0-9]{3})([\D])([0-9]{5})$", num)
                    part_1_pass_number = pass_number.group(1)
                    part_3_pass_number = pass_number.group(3)
                    hex_s = hex(int(part_1_pass_number))[2:]
                    mask.append(hex_s)
                    hex_n = hex(int(part_3_pass_number))[2:]
                    mask.append(hex_n)
                    hex_pass_number = ''.join(mask).upper()
            case _:
                pass
        if len(hex_pass_number) > 12:
            ind_trim = len(hex_pass_number) - 12
            hex_pass_number = hex_pass_number[ind_trim:]
        else:
            count = 12 - len(hex_pass_number)
            hex_pass_number = f'{"0"*count}{hex_pass_number}'

        self.pass_cart_hex_format = hex_pass_number


    def __str__(self) -> str:
        return self.pass_card_dec_format
    

from django.core.cache import cache 

# @property как идея сделать это 
def card_operations(obj, card, type_oper_card):
    oper_card = {
        "id": 0,
        "operation": "del_cards", # del_cards | add_cards
        "cards": [
            # {"card":"000000A2BA93", "flags": 0, "tz": 255},
        ]
    }
    staff_checkpoint_access_dany = obj.access_profile.checpoint.all()
    staff_sn_controller_access_dany = []

    for checkpoint in staff_checkpoint_access_dany:
        staff_sn_controller_access_dany.extend(
            checkpoint.controller_set.all()
        )
    staff_cards = [
        {"card": card, "flags": 0, "tz": 255}]
    oper_card['operation'] = type_oper_card
    oper_card['cards'] = staff_cards
    for contr in staff_sn_controller_access_dany:
        value = cache.get(f'{contr.serial_number}_{type_oper_card}')
        if value != None:
            for el in value:
                if 'cards' in el:
                    el['cards'].append({"card": card, "flags": 0, "tz": 255})
                    cache.set(f'{contr.serial_number}_{type_oper_card}', [el], timeout=15)
        else:
            cache.set(f'{contr.serial_number}_{type_oper_card}', [oper_card], timeout=15)


# DRY !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@receiver(pre_save, sender=CardPass)
def pre_add_card(sender, instance, *args, **kwargs):
    try:
        old_value_card = str(CardPass.objects.get(pk=instance.pk).pass_cart_hex_format)
        print(f'[==INFO==] Изменение карты {instance} сотрудника {instance.staff}.')
        print(f'[==INFO==] |-->> Удаление карты {old_value_card} с контроллеров.')
        print(f'[==INFO==] |-->> Добавление карты {instance} в контроллеры.')
        card_operations(instance.staff, old_value_card, 'del_cards')
    except:
        pass

@receiver(post_save, sender=CardPass)
def add_card(sender, instance, **kwargs):

    if instance.activate_card:
        print(f'[==INFO==] Добавление карты {instance} в контроллеры.')
        card_operations(instance.staff, instance.pass_cart_hex_format, 'add_cards')
    else:
        print(f'[==INFO==] Деактивация карты {instance}.')
        card_operations(instance.staff, instance.pass_cart_hex_format, 'del_cards')


@receiver(post_delete, sender=CardPass)
def delete_card(sender, instance, **kwargs):
    print(f'[==INFO==] Удаление карты {instance} с контроллеров.')
    card_operations(instance.staff, instance.pass_cart_hex_format, 'del_cards')
