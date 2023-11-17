from django.contrib import admin

from django.conf import settings
from django.utils.html import mark_safe

from app_staffs.models import Staff
from app_card_pass.models import CardPass

from app_card_pass.admin import CardPassInlines
from app_photo_staff.admin import StaffPhotoInlines

# from app_staffs.lookups import StaffModelForm


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = [
        'get_photo_staff', 'first_name', 'last_name', 'patromic', 
        'interception',
    ]
    filter_horizontal = ['tag',]
    autocomplete_fields = ['position', 'departament']
    inlines = [CardPassInlines, StaffPhotoInlines]


    def save_related(self, request, form, formsets, change):
        # для конвертирования из DEC в HEX и 
        # запись в поле pass_cart_hex_format CardPass
        form.save_m2m()
        for formset in formsets:
            instances = formset.save(commit=False)
            try:
                obj = instances[0]
                if isinstance(obj, CardPass):
                    for instance in instances:
                        instance.formatting_in_hex
            except IndexError:
                pass
            self.save_formset(request, form, formset, change=change)

    
    def get_photo_staff(self, obj):
        try:
            url_prod = obj.staffphoto_set.all()[0].photo.url
            return mark_safe(f'<img src={url_prod} width="75"')
        except IndexError:
            return mark_safe(f'<img src={settings.NO_PROFILE_PHOTO} width="75"')
    get_photo_staff.short_description = 'ФОТО'
