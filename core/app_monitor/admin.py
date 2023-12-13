from django.contrib import admin
from django.urls import re_path, reverse
from django.utils.html import format_html
from django.shortcuts import render

from app_monitor.models import Monitor


@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = [
        'monitor_name', 
        'account_actions',
    ]
    filter_horizontal = ['monitor_checkpoint',]


    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            re_path(
                r'surveillance/(?P<serial_number_ch>.+)$',
                self.admin_site.admin_view(self.index_view),
                name='checkpoint_monitor',
            ),
        ]
        return custom_urls + urls
    

    def account_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">МОНИТОР</a> ',
            reverse('admin:checkpoint_monitor', args=[obj.pk]),
        )
    account_actions.short_description = 'Мониторы проходных'
    account_actions.allow_tags = True


    def index_view(self, request, *args, **kwargs):
        id = request.META["HTTP_UPGRADE_INSECURE_REQUESTS"]
        checkpoints_this_monitor = self.get_object(request, id).monitor_checkpoint.all()
        list_name_checkpoints = [
            checkpoint.name_checpoint for checkpoint in checkpoints_this_monitor
        ]
        return render(request, 'app_monitor/test.html', {
            'list_name_checkpoints': list_name_checkpoints
        })
    