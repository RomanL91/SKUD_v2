from django.contrib import admin

from app_event.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        'event_staff',
        'event_date_time',
        'event_checkpoint',
        'event_direction',
        'event_granted',
    ]
