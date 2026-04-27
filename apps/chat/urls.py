from django.urls import path
from .views import (
    CreateUserChatView,
    SendUserMessageView,
    GetUserMessagesView,
    UserChatListView
)

urlpatterns = [
    path("userchat/create/", CreateUserChatView.as_view()),
    path("userchat/<int:chat_id>/send/", SendUserMessageView.as_view()),
    path("userchat/<int:chat_id>/messages/", GetUserMessagesView.as_view()),
    path("userchat/", UserChatListView.as_view()),
]