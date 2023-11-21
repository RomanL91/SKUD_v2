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
    monday_time_stert =  models.TimeField(
        choices=get_time_choices(), verbose_name=ver_name_start_d, blank=True, null=True,)
    monday_time_end =  models.TimeField(
        choices=get_time_choices(), verbose_name=ver_name_end_d, blank=True, null=True,)
    
    tuesday_time_start =  models.TimeField(
        choices=get_time_choices(), verbose_name=ver_name_start_d, blank=True, null=True,)
    tuesday_time_end =  models.TimeField(
        choices=get_time_choices(), verbose_name=ver_name_end_d, blank=True, null=True,)
    
    wednesday_time_start = models.TimeField(
        choices=get_time_choices(), verbose_name=ver_name_start_d, blank=True, null=True,)
    wednesday_time_end = models.TimeField(
        choices=get_time_choices(), verbose_name=ver_name_end_d, blank=True, null=True,)
    
    thursday_time_start = models.TimeField(
        choices=get_time_choices(), verbose_name=ver_name_start_d, blank=True, null=True,)
    thursday_time_end = models.TimeField(
        choices=get_time_choices(), verbose_name=ver_name_end_d, blank=True, null=True,)
    
    friday_time_start = models.TimeField(
        choices=get_time_choices(), verbose_name=ver_name_start_d, blank=True, null=True,)
    friday_time_end = models.TimeField(
        choices=get_time_choices(), verbose_name=ver_name_end_d, blank=True, null=True,)
    
    saturday_time_start = models.TimeField(
        choices=get_time_choices(), verbose_name=ver_name_start_d, blank=True, null=True,)
    saturday_time_end = models.TimeField(
        choices=get_time_choices(), verbose_name=ver_name_end_d, blank=True, null=True,)
    
    sunday_time_start = models.TimeField(
        choices=get_time_choices(), verbose_name=ver_name_start_d, blank=True, null=True,)
    sunday_time_end = models.TimeField(
        choices=get_time_choices(), verbose_name=ver_name_end_d, blank=True, null=True,)


    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'


    def __str__(self) -> str:
        return self.name_schedule
