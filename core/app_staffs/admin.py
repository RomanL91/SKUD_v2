from django.contrib import admin

from django.conf import settings
from django.utils.html import mark_safe

from app_staffs.models import Staff
from app_card_pass.models import CardPass

from app_card_pass.admin import CardPassInlines
from app_photo_staff.admin import StaffPhotoInlines

from django.core.cache import cache 

# from app_staffs.lookups import StaffModelForm


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

    def save_model(self, request, obj, form, change):
        if change:
            try:
                form.data['interception']
                self.set_interception(obj, 'del_cards')
                print(f'[==INFO==] Активирую перехват {obj}')
            except KeyError:
                print(f'[==INFO==] Возобновляю доступ для {obj}')
                self.set_interception(obj, 'add_cards')
        else:
            self.set_interception(obj, 'add_cards')

        obj.save()

    
    def delete_model(self, request, obj):
        self.set_interception(obj, 'del_cards')
        obj.delete()

    
    def set_interception(self, obj, type_oper_card):
        oper_card = {
            "id": 0,
            "operation": "del_cards", # del_cards | add_cards
            "cards": [
                # {"card":"000000A2BA93", "flags": 0, "tz": 255},
            ]
        }
        staff_checkpoint_access_dany = obj.access_profile.checpoint.all()
        staff_sn_controller_access_dany = []

        for checkpoint in staff_checkpoint_access_dany:
            staff_sn_controller_access_dany.extend(
                checkpoint.controller_set.all()
            )
        staff_cards = [
            {"card": card.pass_cart_hex_format, "flags": 0, "tz": 255} for card in obj.cardpass_set.all()
        ]
        oper_card['operation'] = type_oper_card
        oper_card['cards'] = staff_cards
        for contr in staff_sn_controller_access_dany:
            cache.set(contr.serial_number, [oper_card], timeout=15)


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
