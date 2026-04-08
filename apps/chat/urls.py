from django.urls import path
from .views import *

urlpatterns = [
    path("chat/start/", GetOrCreateChatView.as_view()),
    path("chat/<int:chat_id>/messages/", GetMessagesView.as_view()),
    path("chat/<int:chat_id>/send/", SendMessageView.as_view()),

    # 🔥 NEW ADMIN ROUTE
    path("chat/admin/chats/", AdminChatListView.as_view()),
]