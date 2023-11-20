from django.contrib import admin

from app_position.models import Position


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ['name_position',]
    filter_horizontal = ['tag',]
