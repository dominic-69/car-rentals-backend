from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [

 
    re_path(r'ws/userchat/(?P<chat_id>\d+)/$', ChatConsumer.as_asgi()),
 
    re_path(r'ws/chat/(?P<chat_id>\d+)/$', ChatConsumer.as_asgi()),

 
    re_path(r'ws/chat/booking_updates/$', ChatConsumer.as_asgi()),
]