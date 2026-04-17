from django.urls import path
from .views import (
    GetOrCreateChatView,
    SendMessageView,
    GetMessagesView,
    AdminChatListView
)

urlpatterns = [
    path("start/", GetOrCreateChatView.as_view()),
    path("<int:chat_id>/messages/", GetMessagesView.as_view()),
    path("<int:chat_id>/send/", SendMessageView.as_view()),
    path("admin/chats/", AdminChatListView.as_view()),
]