from django.contrib import admin

from app_staffs.models import Staff
from app_card_pass.models import CardPass


class CardPassInlines(admin.StackedInline):
    model = CardPass
    extra = 0
    classes = ['collapse']


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    inlines = [CardPassInlines,]


    def save_related(self, request, form, formsets, change):
        # для конвертирования из DEC в HEX и 
        # запись в поле pass_cart_hex_format CardPass
        form.save_m2m()
        for formset in formsets:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.formatting_in_hex
            self.save_formset(request, form, formset, change=change)
