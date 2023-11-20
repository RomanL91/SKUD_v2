from django.contrib import admin

from app_controller.models import Controller
from app_controller.forms import ControllerAdminForm


@admin.register(Controller)
class ControllerAdmin(admin.ModelAdmin):
    form = ControllerAdminForm
    list_display = [
        'name_controller', 'serial_number', 'controller_activity', 
        'controller_online', 'ip_adress', 'manual_control', 
    ]
    autocomplete_fields = ['checkpoint',]
