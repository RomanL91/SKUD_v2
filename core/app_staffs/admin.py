from django.contrib import admin

from app_staffs.models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    pass
