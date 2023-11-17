from django.contrib import admin

from app_departament.models import Departament


@admin.register(Departament)
class DepartamentAdmin(admin.ModelAdmin):
    pass
