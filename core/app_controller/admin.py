from django.contrib import admin

from app_controller.models import Controller
from app_controller.forms import ControllerAdminForm


@admin.register(Controller)
class ControllerAdmin(admin.ModelAdmin):
    form = ControllerAdminForm
    list_display = [
        'serial_number', 'type_controller', 'name_controller',  
        # 'controller_activity', 
        'direction', 
        'ip_adress', 'manual_control', 
    ]
    autocomplete_fields = ['checkpoint',]
    readonly_fields = ['serial_number', 'type_controller']
    fieldsets = (
        ('Контроллер', {'fields': (('serial_number', 'type_controller'), ('name_controller', 'ip_adress'))}),
        ('Состояние/Режим', {'fields': (('controller_activity', 'controller_online', 'controller_mode'), 'manual_control')}),
        ('Проходная/Направление', {'fields': (('checkpoint', 'direction',),)}),
    )
