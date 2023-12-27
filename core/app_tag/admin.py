from django.contrib import admin

from django import forms
from django.utils.html import format_html

from app_tag.models import Tags, ColorField
from app_staffs.models import Staff

from django.core.cache import cache 


@admin.register(Tags)
class TagAdmin(admin.ModelAdmin):
    list_display = [
        'get_color_tag', 'name_tag', 'desc_tag', 'interception', 
    ]
    formfield_overrides = {
        ColorField: {'widget': forms.TextInput(attrs={'type': 'color'})}
    }


    def get_color_tag(self, obj):
        return format_html(
            '''<div style="background-color:{}; width:30px; height:30px">
            </div>''',
            obj.color_tad,
        )
    get_color_tag.short_description = 'Цвет'


    def save_model(self, request, obj, form, change):
        objs_to_update = set()
        all_staffs_this_tag = obj.staff_set.all()
        all_position_this_tag = obj.position_set.all()

        for staff in all_staffs_this_tag:
            staff.interception = obj.interception
            objs_to_update.add(staff)

        for position in all_position_this_tag:
            for staff in position.staff_set.all():
                staff.interception = obj.interception
                objs_to_update.add(staff)

        if change:
            try:
                form.data['interception']
                for staff in objs_to_update:
                    self.set_interception(staff, 'del_cards')
            except KeyError:
                for staff in objs_to_update:
                    self.set_interception(staff, 'add_cards')

        Staff.objects.bulk_update(objs_to_update, ['interception'])
        obj.save()


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
