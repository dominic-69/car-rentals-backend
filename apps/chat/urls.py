from django.urls import path
from .views import (
    # 🔥 EXISTING (DO NOT TOUCH)
    GetOrCreateChatView,
    SendMessageView,
    GetMessagesView,
    AdminChatListView,

    # 🔥 NEW (USER ↔ USER)
    CreateUserChatView,
    GetUserMessagesView,
    SendUserMessageView,
    UserChatListView
)

urlpatterns = [
    path("start/", GetOrCreateChatView.as_view()),
    path("<int:chat_id>/messages/", GetMessagesView.as_view()),
    path("<int:chat_id>/send/", SendMessageView.as_view()),
    path("admin/chats/", AdminChatListView.as_view()),
    path("userchat/<int:chat_id>/send/", SendUserMessageView.as_view()),
    path("userchat/", UserChatListView.as_view()),


    path("userchat/create/", CreateUserChatView.as_view()),
    path("userchat/<int:chat_id>/messages/", GetUserMessagesView.as_view()),
]