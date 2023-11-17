from django.db import models


class Controller(models.Model):
    name_controller = models.CharField(
        verbose_name='Имя контроллера', max_length=200,
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
        verbose_name='Состояние контроллера', max_length=10,  default='0',
        help_text='''
        Выбирите состояние контроллера и сохраните его <br>
        для включения или выключения.
        '''
    )
    controller_online = models.CharField(
        verbose_name='Режимы контроллера', max_length=10, default='0')
    # проходная
    # активность (вкл\выкл)
    # режимы онлайн
    # режимы работы
    # 