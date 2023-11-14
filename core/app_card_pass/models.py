from django.db import models

from app_staffs.models import Staff


class CardPass(models.Model):
    # 
    # фото карты?
    # 
    pass_card_dec_format = models.CharField(
        verbose_name='Номер пропуска в DEC формате', max_length=10, unique=True
    )
    pass_cart_hex_format = models.CharField(
        verbose_name='Номер пропуска в HEX формате', max_length=10, blank=True,
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


    def __str__(self) -> str:
        return self.pass_card_dec_format
    