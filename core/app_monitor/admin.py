from django.contrib import admin

from app_monitor.models import Monitor


@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    pass
