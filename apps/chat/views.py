from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .models import UserChat, UserMessage

User = get_user_model()


# =========================
# 🔥 CREATE CHAT (USER ↔ USER)
# =========================

class CreateUserChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        other_user_id = request.data.get("user_id")

        try:
            other_user = User.objects.get(id=other_user_id)

            # check existing chat
            chat = UserChat.objects.filter(
                user1=user, user2=other_user
            ).first() or UserChat.objects.filter(
                user1=other_user, user2=user
            ).first()

            # create if not exists
            if not chat:
                chat = UserChat.objects.create(
                    user1=user,
                    user2=other_user
                )

            return Response({"chat_id": chat.id})

        except User.DoesNotExist:
            return Response({"error": "User not found ❌"}, status=404)


# =========================
# 🔥 SEND MESSAGE
# =========================

class SendUserMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, chat_id):
        text = request.data.get("message")

        if not text:
            return Response({"error": "Message empty ❌"}, status=400)

        UserMessage.objects.create(
            chat_id=chat_id,
            text=text,
            sender_name=request.user.username
        )

        return Response({"msg": "sent"})


# =========================
# 🔥 GET MESSAGES
# =========================

class GetUserMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, chat_id):
        messages = UserMessage.objects.filter(
            chat_id=chat_id
        ).order_by("created_at")

        data = []

        for msg in messages:
            data.append({
                "text": msg.text,
                "sender": msg.sender_name,
                "status": msg.status,
                "created_at": msg.created_at,
            })

        return Response(data)


# =========================
# 🔥 CHAT LIST (LEFT PANEL)
# =========================

class UserChatListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        chats = UserChat.objects.filter(user1=user) | UserChat.objects.filter(user2=user)

        data = []

        for chat in chats:
            other_user = chat.user2 if chat.user1 == user else chat.user1

            last_msg = UserMessage.objects.filter(chat=chat).order_by("-created_at").first()

            data.append({
                "id": chat.id,
                "other_user_name": other_user.username,
                "last_message": last_msg.text if last_msg else ""
            })

        return Response(data)