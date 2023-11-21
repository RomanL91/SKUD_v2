from django.contrib import admin

from app_shedule.models import Schedule, Day

from app_shedule.forms import ScheduleAdminForm, DayAdminForm


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    form = ScheduleAdminForm


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    form = DayAdminForm
