from django.contrib import admin

from app_card_pass.models import CardPass


@admin.register(CardPass)
class CardPassAdmin(admin.ModelAdmin):
    pass
