from django.contrib import admin

from app_controller.models import Controller
from app_controller.forms import ControllerAdminForm


@admin.register(Controller)
class ControllerAdmin(admin.ModelAdmin):
    form = ControllerAdminForm
