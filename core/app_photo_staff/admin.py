from django.contrib import admin

from app_photo_staff.models import StaffPhoto


@admin.register(StaffPhoto)
class StaffPhotoAdmin(admin.ModelAdmin):
    pass
