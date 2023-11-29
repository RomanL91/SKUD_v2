import re

from django.db import models

from app_staffs.models import Staff

from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _


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
    # 
    # фото карты?
    # 
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
        self.save()

    @property
    def send_card_to_controller(self):
        from core.utils import BaseAdapterForModels
        adapter = BaseAdapterForModels()
        print(self)
        print(self.staff)
        print(self.staff.access_profile)
        print(self.staff.access_profile.checpoint)
        # print(self.staff.access_profile.checpoint_set.all())


    def __str__(self) -> str:
        return self.pass_card_dec_format
    