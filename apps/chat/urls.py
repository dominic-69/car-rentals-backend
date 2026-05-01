from django.urls import path
from .views import (
    CreateUserChatView,
    SendUserMessageView,
    GetUserMessagesView,
    UserChatListView,
    StartAdminSellerChatView,
    AdminChatsView,
)

urlpatterns = [
    # =========================
    # 🔥 USER ↔ USER (OLD - KEEP)
    # =========================
    path("userchat/create/", CreateUserChatView.as_view()),
    path("userchat/<int:chat_id>/send/", SendUserMessageView.as_view()),
    path("userchat/<int:chat_id>/messages/", GetUserMessagesView.as_view()),
    path("userchat/", UserChatListView.as_view()),

 
    path("admin-seller/start/", StartAdminSellerChatView.as_view()),

    # =========================
    # 🔥 ALIAS ROUTES (IMPORTANT FIX)
    # =========================
    path("<int:chat_id>/messages/", GetUserMessagesView.as_view()),  # ✅ FIX 404
    path("<int:chat_id>/send/", SendUserMessageView.as_view()),      # optional
    path("admin/chats/", AdminChatsView.as_view()),
]