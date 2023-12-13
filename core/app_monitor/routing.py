from django.urls import re_path

from app_monitor.consumers import WebClientConsumer

websocket_urlpatterns = [
    re_path(r'ws/sc/', WebClientConsumer.as_asgi()),
]
