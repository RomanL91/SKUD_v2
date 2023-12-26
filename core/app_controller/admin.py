from django.contrib import admin

from app_controller.models import Controller
from app_controller.forms import ControllerAdminForm

from django.core.cache import cache 


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


    def save_model(self, request, obj, form, change):
        # возможно правильнее отработать (получение полей) через адаптер, пока для быстрого решения
        set_mode: dict = {"id": 0, "operation": "set_mode", "mode": None}
        set_active: dict = {"id": 0, "operation": "set_active", "active": None, "online": None}

        set_active['active'] = int(obj.controller_activity)
        set_active['online'] = int(obj.controller_online)
        set_mode['mode'] = int(obj.controller_mode)

        message_reply = [set_active, set_mode]

        cache.set(obj.serial_number, message_reply, timeout=15) #хардкодно время хранения в кеше состояние режимов контроллера

        obj.save()
