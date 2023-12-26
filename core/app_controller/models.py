from django.db import models

from app_checkpoint.models import Checkpoint


class Controller(models.Model):
    name_controller = models.CharField(
        verbose_name='Имя контроллера', max_length=200, unique=False,
        help_text='''
        Дайте контроллеру обдуманное и рациональное имя,<br>
        которое ВЫ будете дальше использовать в системе в целом.<br>
        Это важно и для Вашего удобства дальнейшего использования.
        '''
    )
    ip_adress = models.URLField(
        verbose_name='URL', max_length=200,
        help_text='''
        Введите адресс программного обеспечения,<br>
        с которым работают контроллеры.
        '''
    )
    type_controller = models.CharField(
        verbose_name='Тип контроллера', max_length=200,
    )
    serial_number = models.CharField(
        verbose_name='Серийный номер контроллера', max_length=200,
        unique=True
    )
    manual_control = models.BooleanField(
        verbose_name='Ручное управление', default=False,
        help_text='''
        При выборе данного свойства смена ркжима или отключение<br>
        контроллера возможна только в ручном режиме, через Админ интерфейс.<br>
        Никакие другие ПО или скрипты не смогут управлять состоянием контроллера.
        '''
    )
    controller_activity = models.CharField(
        verbose_name='Состояние контроллера', max_length=10,  default='1',
        help_text='''
        Выбирите состояние контроллера и сохраните его <br>
        для включения или выключения.
        '''
    )
    controller_online = models.CharField(
        verbose_name='Режимы контроллера', max_length=10, default='1'
    )
    controller_mode = models.CharField(
        verbose_name='Режим контроллера', max_length=10, default='1'
    )
    checkpoint = models.ForeignKey(
        Checkpoint, on_delete=models.CASCADE, 
        verbose_name='Проходная', blank=True, null=True,
        help_text='''Выберите проходную, к которой приявяжете контроллер.<br>
        Контроллер без выбранной проходной не учавствует в логике программы.<br>
        События с такого контроллера не сохраняются в системе и полностью игнорируются.
        '''
    )
    direction = models.CharField(
        verbose_name='Направление', max_length=30, default='0', blank=True,
        help_text='''
        Установите направление контроллера.<br>
        Другими словами укажите с какой стороны находится контроллер:<br>
        со стороны входа или стороны выхода с территории/из помещения<br>
        или же контроллер один на проходную (Контроллер на ВХОД и ВЫХОД).
        '''
    )

    class Meta:
        verbose_name = 'Контроллер'
        verbose_name_plural = 'Контроллеры'


    def __str__(self) -> str:
        return self.name_controller
    

    @property
    def get_serial_number_type_int(self):
        return int(self.serial_number)
