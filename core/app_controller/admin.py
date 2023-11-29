from django.contrib import admin

from app_controller.models import Controller
from app_controller.forms import ControllerAdminForm

from core.utils import BaseAdapterForModels


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
        ('Состояние/Режим', {'fields': (('controller_activity', 'controller_online', ), 'manual_control')}),
        ('Проходная/Направление', {'fields': (('checkpoint', 'direction',),)}),
    )


    def save_model(self, request, obj, form, change):
        adapter = BaseAdapterForModels()

        adapter.set_active['active'] = int(obj.controller_activity)
        adapter.set_active['online'] = int(obj.controller_online.split('/')[0])
        adapter.set_mode['mode'] = int(obj.controller_online.split('/')[1])
        
        message_reply = [adapter.set_active, adapter.set_mode]
        payload = adapter.response_model(message_reply, obj.serial_number)
        adapter.send_signal(obj.ip_adress, payload) # выгружать в фон мультипроцессинг или целери

        obj.save()
