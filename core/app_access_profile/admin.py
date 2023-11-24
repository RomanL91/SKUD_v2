from django.contrib import admin

from app_access_profile.models import AccessProfile
from app_staffs.models import Staff


@admin.register(AccessProfile)
class AccessProfilrAdmin(admin.ModelAdmin):
    list_display = [
        'name_access_profile', 'block_access_profile', 'desc_access_profile'
    ]
    filter_horizontal = [
        'checpoint',
    ]
    search_fields = ['name_access_profile',]

    def save_model(self, request, obj, form, change):
        all_staffs_this_dep = obj.staff_set.all()
        objs_to_update = []
        for staff in all_staffs_this_dep:
            staff.interception = obj.block_access_profile
            objs_to_update.append(staff)
        Staff.objects.bulk_update(objs_to_update, ['interception'])
        obj.save()
