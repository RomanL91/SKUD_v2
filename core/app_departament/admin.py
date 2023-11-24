from django.contrib import admin

from app_departament.models import Departament
from app_staffs.models import Staff


@admin.register(Departament)
class DepartamentAdmin(admin.ModelAdmin):
    search_fields = ['name_departament']
    list_display = ['name_departament', 'interception', 'desc_dep']

    def save_model(self, request, obj, form, change):
        if 'interception' in form.data:
            objs_to_update = []
            all_staffs_this_dep = obj.staff_set.all()
            for staff in all_staffs_this_dep:
                staff.interception = obj.interception
                objs_to_update.append(staff)
            Staff.objects.bulk_update(objs_to_update, ['interception'])
        obj.save()
