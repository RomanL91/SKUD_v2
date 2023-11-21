from django.contrib import admin

from app_shedule.models import Schedule, Day


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    pass


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    pass
