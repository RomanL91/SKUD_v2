from django.contrib import admin

from app_event.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
