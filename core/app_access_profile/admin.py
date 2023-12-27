from django.contrib import admin

from app_access_profile.models import AccessProfile
from app_staffs.models import Staff

from django.core.cache import cache 


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
        if change:
            try:
                form.data['block_access_profile']
                block_access_profile = True
            except KeyError:
                block_access_profile = False

            all_staffs_this_dep = obj.staff_set.all()
            objs_to_update = []
            for staff in all_staffs_this_dep:
                staff.interception = obj.block_access_profile
                objs_to_update.append(staff)
                if block_access_profile:
                    self.set_interception(staff, 'del_cards')
                else:
                    self.set_interception(staff, 'add_cards')
            Staff.objects.bulk_update(objs_to_update, ['interception'])
        obj.save()


    def delete_model(self, request, obj):
        # TO DO!!!!!!!!!!!!!!!!
        """
        ПРИ УДАЛЕНИИ ПРОФИЛЯ ДОСТУПА, ЧТО ДЕЛАТЬ С КАРТАМИ ЭТОГО ПРОФИЛЯ??????
        """
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
