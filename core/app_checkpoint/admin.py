from django.contrib import admin

from app_checkpoint.models import Checkpoint


@admin.register(Checkpoint)
class CheckpointAdmin(admin.ModelAdmin):
    pass
