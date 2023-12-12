from django.db import models

from app_checkpoint.models import Checkpoint
from app_event.models import Event


class Monitor(models.Model):
    monitor_name = models.CharField(
        verbose_name='Имя монитора', max_length=125,
        default='Монитор [-укажи имя-]',
        # help_text=
    )
    monitor_checkpoint = models.ManyToManyField(
        Checkpoint, blank=True,
        verbose_name='Проходные для монитора'
        # help_text=
    )

    class Meta:
        verbose_name = 'Монитор'
        verbose_name_plural = 'Мониторы'


    def __str__(self) -> str:
        return self.monitor_name
