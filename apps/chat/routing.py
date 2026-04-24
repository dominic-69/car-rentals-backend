from django.urls import re_path
from .consumers import UserChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/userchat/(?P<chat_id>\d+)/$', UserChatConsumer.as_asgi()),
]