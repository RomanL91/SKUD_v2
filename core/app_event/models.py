from django.db import models

from django.dispatch import receiver
from django.db.models.signals import post_save

import channels.layers
from asgiref.sync import async_to_sync


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
        blank=True, null=True,
    )
    event_card_dec = models.CharField(
        verbose_name='Карта инициатор события dec', max_length=15,
        blank=True, null=True,
    )
    event_staff = models.CharField(
        verbose_name='Сотрудник инициатор события', max_length=200,
        blank=True, null=True,
    )
    event_controller = models.CharField(
        verbose_name='Контроллер инициатор события', max_length=200,
        blank=True, null=True,
    )
    event_checkpoint = models.CharField(
        verbose_name='Проходная иницитор события', max_length=200,
        blank=True, null=True,
    )
    event_direction = models.CharField(
        verbose_name='Направление события', max_length=30,
        blank=True, null=True,
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
        verbose_name='Решение по доступу для события', default=False,
    )
    event_package = models.JSONField(
        verbose_name='Присланный пакет события', default=dict,
    )
    event_reason_granted = models.CharField(
        verbose_name='Тип решения по доступу', max_length=200,
        default='тип не определен', blank=True, null=True
    )
    late = models.BooleanField(
        verbose_name='Опоздание??', default=False
    )
    event_late_status = models.CharField(
        verbose_name='Статус опоздания', max_length=250,
        blank=True, null=True, default='Без нарушений графика'
    )
    ENTRY_EXIT_queue_broken = models.BooleanField(
        verbose_name='Нарушение очередности  входа и выхода',
        default=False,
        help_text='''
        Данное поле активно в случаях, когда нарушается очередность событий.<br>
        Например: Сотрудник выходит с территории (ВЫХОД), а события входа (ВХОД)<br>
        нет в системе за сегодняшний день. И соотвественно наоборот.<br>
        Всегда ожидается цепочка событий типа: ВХОД -> ВЫХОД -> ВХОД -> ВЫХОД и т.д.
        '''
    )

    
    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self) -> str:
        return self.event_staff


from app_event.serializers import EventSerializer


@receiver(post_save, sender=Event)
def send_message(sender, instance, **kwargs):
    data = EventSerializer(instance).data
    channels_ = channels.layers.get_channel_layer()
    async_to_sync(channels_.group_send)("client", {"type": "receive", "text_data": {"data": data}})
    