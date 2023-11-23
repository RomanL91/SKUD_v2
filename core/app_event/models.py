from django.db import models


class Event(models.Model):
    event_class = models.CharField(
        verbose_name='Класс события', max_length=15,
    )
    event_date_time = models.DateTimeField(
        verbose_name='Дата и время события',
        # auto_created=
    )
    event_card_hex = models.CharField(
        verbose_name='Карта инициатор события (hex)', max_length=15,
    )
    event_card_dec = models.CharField(
        verbose_name='Карта инициатор события dec', max_length=15,
    )
    event_staff = models.CharField(
        verbose_name='Сотрудник инициатор события', max_length=200,
    )
    event_controller = models.CharField(
        verbose_name='Контроллер инициатор события', max_length=200,
    )
    event_checkpoint = models.CharField(
        verbose_name='Проходная иницитор события', max_length=200
    )
    event_direction = models.CharField(
        verbose_name='Направление события', max_length=30,
    )
    event_type = models.CharField(
        verbose_name='Тип события (код от контроллера)', max_length=5,
        blank=True, null=True,
    )
    event_flag = models.CharField(
        verbose_name='Флаг события', max_length=5,
        blank=True, null=True,
    )
    event_granted = models.BooleanField(
        verbose_name='Разрешение доступа для события', default=False,
    )
    event_package = models.JSONField(
        verbose_name='Присланный пакет события', default=dict,
    )

    
    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self) -> str:
        return self.event_staff


    

