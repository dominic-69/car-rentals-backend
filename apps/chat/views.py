from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

from .models import Chat, Message, UserChat, UserMessage
from .serializers import MessageSerializer, UserMessageSerializer

User = get_user_model()


# =========================
# 🔥 ADMIN ↔ SELLER CHAT (KEEP SAME)
# =========================

class GetOrCreateChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        admin = user.__class__.objects.filter(role="admin").first()

        chat, created = Chat.objects.get_or_create(
            seller=user,
            admin=admin
        )

        return Response({"chat_id": chat.id})


class SendUserMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, chat_id):
        text = request.data.get("message")
        sender = request.user.username

        UserMessage.objects.create(
            chat_id=chat_id,
            text=text,
            sender_name=sender
        )

        return Response({"msg": "sent"})


class GetMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, chat_id):
        messages = Message.objects.filter(chat_id=chat_id).order_by("created_at")
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class AdminChatListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "admin":
            return Response({"error": "Unauthorized ❌"}, status=403)

        chats = Chat.objects.all().order_by("-created_at")

        data = []
        for chat in chats:
            data.append({
                "chat_id": chat.id,
                "seller_id": chat.seller.id,
                "seller_name": chat.seller.username,
            })

        return Response(data)


# =========================
# 🔥 USER ↔ USER CHAT (NEW)
# =========================

from django.contrib.auth import get_user_model
from .models import UserChat, UserMessage
from .serializers import UserMessageSerializer

User = get_user_model()


class CreateUserChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        other_user_id = request.data.get("user_id")

        try:
            other_user = User.objects.get(id=other_user_id)

            # 🔥 CHECK EXISTING CHAT
            chat = UserChat.objects.filter(
                user1=user, user2=other_user
            ).first() or UserChat.objects.filter(
                user1=other_user, user2=user
            ).first()

            # 🔥 CREATE IF NOT EXISTS
            if not chat:
                chat = UserChat.objects.create(
                    user1=user,
                    user2=other_user
                )

            return Response({"chat_id": chat.id})

        except User.DoesNotExist:
            return Response({"error": "User not found ❌"}, status=404)


class GetUserMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, chat_id):
        messages = UserMessage.objects.filter(chat_id=chat_id).order_by("created_at")

        data = []
        for msg in messages:
            data.append({
                "text": msg.text,
                "sender": msg.sender_name,
                "status": msg.status,
                "created_at": msg.created_at,
            })

        return Response(data)
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserChat, UserMessage


class UserChatListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        chats = UserChat.objects.filter(
            user1=user
        ) | UserChat.objects.filter(
            user2=user
        )

        data = []

        for chat in chats:
            # 🔥 find other user
            other_user = chat.user2 if chat.user1 == user else chat.user1

            # 🔥 last message
            last_msg = UserMessage.objects.filter(chat=chat).order_by("-created_at").first()

            data.append({
                "id": chat.id,
                "other_user_name": other_user.username,
                "last_message": last_msg.text if last_msg else "",
            })

        return Response(data)
    
# =========================
# 🔥 ADMIN ↔ SELLER SEND MESSAGE (FIX)
# =========================
class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, chat_id):
        text = request.data.get("message")
        sender = request.user.username

        Message.objects.create(
            chat_id=chat_id,
            text=text,
            sender_name=sender
        )

        return Response({"msg": "sent"})