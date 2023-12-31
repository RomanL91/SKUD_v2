from django.contrib import admin

from django.conf import settings
from django.utils.html import mark_safe

from app_staffs.models import Staff
from app_card_pass.models import CardPass

from app_card_pass.admin import CardPassInlines
from app_photo_staff.admin import StaffPhotoInlines


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    readonly_fields = [
        'preview_photo_staff',
    ]
    list_display = [
        'get_photo_staff', 'first_name', 'last_name', 'patromic', 
        'interception',
    ]
    filter_horizontal = ['tag',]
    autocomplete_fields = ['position', 'departament', 'access_profile', 'schedule']
    inlines = [CardPassInlines, StaffPhotoInlines]
    fieldsets = (
        ('ФОТО', {'fields': (('preview_photo_staff', ),)}),
        ('Фамилия/Имя/Отчество', {'fields': (('first_name', 'last_name', 'patromic'),)}),
        ('Департамент/Должность/Расписание', {'fields': (('departament', 'position', 'schedule'),),}),
        ('Управление доступом', {'fields': ('access_profile', 'without_biometric_verification', 'interception'),}),
        ('Теги/Подгруппы', {'fields': (('tag',),), 'classes':('collapse',)}),
        ('Остальное о сотруднике', {'fields': (('home_adress', 'phone_number'),), 'classes':('collapse',)}),
    )


    def save_related(self, request, form, formsets, change):
        # для конвертирования из DEC в HEX и 
        # запись в поле pass_cart_hex_format CardPass
        form.save_m2m()
        for formset in formsets:
            instances = formset.save(commit=False)
            for obj in instances:
                if isinstance(obj, CardPass):
                    obj.formatting_in_hex
            self.save_formset(request, form, formset, change=change)


    def preview_photo_staff(self, obj):
        try:
            url_photo = obj.staffphoto_set.all()[0].photo.url
            return mark_safe(f'<img src={url_photo} width="300" ')
        except IndexError:
            return mark_safe(f'<img src={settings.NO_PROFILE_PHOTO} width="300"')
    preview_photo_staff.short_description = 'ФОТО'

    
    def get_photo_staff(self, obj):
        try:
            url_photo = obj.staffphoto_set.all()[0].photo.url
            return mark_safe(f'<img src={url_photo} width="75"')
        except IndexError:
            return mark_safe(f'<img src={settings.NO_PROFILE_PHOTO} width="75"')
    get_photo_staff.short_description = 'ФОТО'
