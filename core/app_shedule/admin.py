from django.contrib import admin
from django.db import models
from django import forms


from app_shedule.models import Schedule, Day

from app_shedule.forms import ScheduleAdminForm, DayAdminForm , CHOICES_WEEK_DAY


class DayInline(admin.StackedInline):
    model = Day
    max_num = 7
    extra = 0
    formfield_overrides = {
        models.CharField: {'widget': forms.Select(choices=CHOICES_WEEK_DAY)}
    }
    classes = ['collapse']


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = [
        'name_schedule', 'type_schedule', 'strict_schedule', 'desc_schedule'
    ]
    form = ScheduleAdminForm
    inlines = [DayInline,]
    fieldsets = (
        (None, {'fields': ('name_schedule', 'desc_schedule')}),
        ('Тип расписания', {'fields': (('type_schedule', 'strict_schedule'),),}),
    )


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = [
        'week_day', 
        'day_time_start', 'day_time_end', 
        'break_in_schedule_start', 'break_in_schedule_end', 
        'schedule'
    ]
    form = DayAdminForm
    fieldsets = (
        (None, {'fields': ('week_day', 'schedule')}),
        ('Начало и конец рабочего дня', {'fields': (('day_time_start', 'day_time_end'),),}),
        ('Начало и конец перерыва', {'fields': (('break_in_schedule_start', 'break_in_schedule_end'),),}),
    )
