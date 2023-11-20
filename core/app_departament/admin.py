from django.contrib import admin

from app_departament.models import Departament


@admin.register(Departament)
class DepartamentAdmin(admin.ModelAdmin):
    search_fields = ['name_departament']
    list_display = ['name_departament', 'interception', 'desc_dep']
