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
