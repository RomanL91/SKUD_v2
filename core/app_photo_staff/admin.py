from django.contrib import admin

from app_photo_staff.models import StaffPhoto

from django.utils.html import mark_safe


@admin.register(StaffPhoto)
class StaffPhotoAdmin(admin.ModelAdmin):
    readonly_fields = ["preview"]
    list_display = [
        'get_image',
        'staff',
        'desc'
    ]
    
    def preview(self, obj):
        print(obj)
        print(obj.photo.url)
        return mark_safe(f'<img src={obj.photo.url} width="600" ')
    preview.short_description = 'Предпоказ'

    
    def get_image(self, obj):
        try:
            url_prod = obj.photo.url
            return mark_safe(f'<img src={url_prod} width="75"')
        except:
            return None
    get_image.short_description = 'ФОТО'
