from django.contrib import admin

from app_card_pass.models import CardPass


class CardPassInlines(admin.StackedInline):
    model = CardPass
    extra = 0
    classes = ['collapse']


@admin.register(CardPass)
class CardPassAdmin(admin.ModelAdmin):
    
    def save_model(self, request, obj, form, change):
        obj.formatting_in_hex
