from django.db import models

from datetime import datetime, time, date, timedelta


ver_name_start_d = 'начало рабочего дня'
ver_name_end_d = 'конец рабочего дня'

def get_time_choices(start_time=time(0,0,0), end_time=time(23,0,0), delta=timedelta(minutes=5)):
    time_choices = ()
    time = start_time
    while time <= end_time:
        time_choices += ((time, time.strftime("%H:%M")),)
        time = (datetime.combine(date.today(), time) + delta).time()
    return time_choices


class Schedule(models.Model):
    name_schedule = models.CharField(
        verbose_name='Название расписания', max_length=200, unique=True,
    )
    desc_schedule = models.TextField(
        verbose_name='Описание расписания', blank=True
    )
    type_schedule = models.CharField(
        verbose_name='Тип расписания', max_length=100,
        help_text='''
        Выберите тип расписания.<br>
        Расписание может быть создано как для Сотрудника, так и для Профиля доступа,<br>
        а так же и для Проходной. Это дает еще один уровень контроля. Например:<br>
        созданное расписание для сотрудников будет опещать дежурного/охрану/вахтера<br>
        о времени действия сотрудника, скажем, сто последний зашел с опозданием или вне графика.<br>
        Создав и добавив расписание для проходной, пост будет информирован о том,<br>
        что событие было совершено согласно расписанию проходной или вне расписания.<br>
        '''
    )
    strict_schedule = models.BooleanField(
        verbose_name='Строгое расписание', default=False,
        help_text='''
        Данный параметр можно применить только к расписанию проходных.<br>
        Если расписание проходной строгое, то проходная будет отказывать в доступе<br>
        при событиях совершенных на ней вне расписания.<br>
        '''
    )


    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'


    def __str__(self) -> str:
        return self.name_schedule
    

class Day(models.Model):
    week_day = models.CharField(
    verbose_name='День недели', max_length=200, default=0)

    break_in_schedule_start = models.TimeField(
        choices=get_time_choices(), verbose_name='Начало перерыва', blank=True, null=True,)
    break_in_schedule_end = models.TimeField(
        choices=get_time_choices(), verbose_name='Конец перерыва', blank=True, null=True,)
    
    day_time_start =  models.TimeField(
        choices=get_time_choices(), verbose_name=ver_name_start_d, blank=True, null=True,)
    day_time_end =  models.TimeField(
        choices=get_time_choices(), verbose_name=ver_name_end_d, blank=True, null=True,)
    
    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE,
        verbose_name='Расписание'
    )


    class Meta:
        verbose_name = 'День'
        verbose_name_plural = 'Дни'
        constraints = (
            models.UniqueConstraint(
                fields=('week_day', 'schedule',), 
                name='%(app_label)s_%(class)s_week_day_schedule'
            ),
        )


    def __str__(self) -> str:
        return self.week_day
