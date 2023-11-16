from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget

from django.conf import settings
from django.utils.html import mark_safe
from django.utils.html import format_html

from django.db import models
from app_photo_staff.models import StaffPhoto


class CustomAdminPhotoWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        result = []
        if hasattr(value, "url"):
            result.append(
                f'''<a href="{value.url}" target="_blank">
                      <img 
                        src="{value.url}" alt="{value}" 
                        width="100" height="100"
                        style="object-fit: cover;"
                      />
                    </a>'''
            )
        result.append(super().render(name, value, attrs, renderer))
        return format_html("".join(result))
    

class StaffPhotoInlines(admin.StackedInline):
    model = StaffPhoto
    extra = 0
    classes = ['collapse']
    formfield_overrides = {
        models.ImageField: {'widget': CustomAdminPhotoWidget}
    }


@admin.register(StaffPhoto)
class StaffPhotoAdmin(admin.ModelAdmin):
    readonly_fields = ["preview",]
    list_display = [
        'get_image', 'staff',  'desc'
    ]
    
    
    def preview(self, obj):
        return mark_safe(f'<img src={obj.photo.url} width="600" ')
    preview.short_description = 'Предпоказ'

    
    def get_image(self, obj):
        try:
            url_prod = obj.photo.url
            return mark_safe(f'<img src={url_prod} width="75"')
        except ValueError:
           return mark_safe(f'<img src={settings.NO_PROFILE_PHOTO} width="75"')
    get_image.short_description = 'ФОТО'
