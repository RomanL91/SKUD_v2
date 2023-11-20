from django.contrib import admin

from app_access_profile.models import AccessProfile


@admin.register(AccessProfile)
class AccessProfilrAdmin(admin.ModelAdmin):
    list_display = [
        'name_access_profile', 'block_access_profile', 'desc_access_profile'
    ]
    filter_horizontal = [
        'checpoint',
    ]
