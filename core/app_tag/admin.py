from django.contrib import admin

from django import forms
from django.utils.html import format_html

from app_tag.models import Tags, ColorField


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
