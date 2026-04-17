from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Chat, Message
from .serializers import MessageSerializer

from .utils import call_fastapi   # ✅ using FastAPI
from .services import smart_car_search


# =========================
# 🔥 CREATE OR GET CHAT
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


# =========================
# 🔥 SEND MESSAGE
# =========================
class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, chat_id):
        text = request.data.get("text")
        user = request.user

        # ✅ Save user/admin/seller message
        Message.objects.create(
            chat_id=chat_id,
            sender=user,
            text=text
        )

        # 🔥 ONLY APPLY AI FOR NORMAL USER
        if user.role == "user":

            # 🔥 Call FastAPI
            reply = call_fastapi(text)

            # 🔁 fallback if FastAPI fails
            if not reply:
                cars = smart_car_search(text)

                if cars:
                    reply = "Here are some cars:\n"
                    for car in cars:
                        reply += f"{car.title} - ₹{car.price}\n"
                else:
                    reply = "No cars found 😔"

            # ✅ Save AI reply
            Message.objects.create(
                chat_id=chat_id,
                sender=user,  # later we can replace with bot user
                text=reply
            )

        return Response({"message": "Sent ✅"})


# =========================
# 🔥 GET MESSAGES
# =========================
class GetMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, chat_id):
        messages = Message.objects.filter(chat_id=chat_id).order_by("created_at")

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


# =========================
# 🔥 ADMIN - GET ALL CHATS
# =========================
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