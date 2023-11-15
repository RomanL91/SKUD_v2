from django.contrib import admin

from app_staffs.models import Staff
from app_card_pass.models import CardPass
from app_photo_staff.models import StaffPhoto


class CardPassInlines(admin.StackedInline):
    model = CardPass
    extra = 0
    classes = ['collapse']


class StaffPhotoInlines(admin.StackedInline):
    model = StaffPhoto
    extra = 0
    classes = ['collapse']


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
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
