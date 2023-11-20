from django.contrib import admin

from app_checkpoint.models import Checkpoint


@admin.register(Checkpoint)
class CheckpointAdmin(admin.ModelAdmin):
    list_display = [
        'name_checpoint', 'checkpoint_block', 'desc_checkpoint',
    ]
    search_fields = [
        'name_checpoint',
    ]
