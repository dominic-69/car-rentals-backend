from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .models import UserChat, UserMessage

User = get_user_model()


        #USER TO USER

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


#  

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
    
    
class StartAdminSellerChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        #  find admin
        admin = User.objects.filter(role="admin").first()

        if not admin:
            return Response({"error": "Admin not found ❌"}, status=404)

        #   if seller → chat with admin
        if user.role == "seller":
            user1, user2 = user, admin

        #   if admin → chat with seller (pass seller_id)
        elif user.role == "admin":
            seller_id = request.data.get("seller_id")
            try:
                seller = User.objects.get(id=seller_id, role="seller")
                user1, user2 = user, seller
            except User.DoesNotExist:
                return Response({"error": "Seller not found ❌"}, status=404)

        else:
            return Response({"error": "Not allowed ❌"}, status=403)

        #    check existing
        chat = UserChat.objects.filter(user1=user1, user2=user2).first() or \
               UserChat.objects.filter(user1=user2, user2=user1).first()

        if not chat:
            chat = UserChat.objects.create(user1=user1, user2=user2)

        return Response({"chat_id": chat.id})
    
class AdminChatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "admin":
            return Response({"error": "Unauthorized ❌"}, status=403)

        chats = UserChat.objects.all().order_by("-id")

        data = []

        for chat in chats:
            # find seller
            seller = chat.user1 if chat.user1.role == "seller" else chat.user2

            data.append({
                "chat_id": chat.id,
                "seller_name": seller.username,
                "seller_id": seller.id,
            })

        return Response(data)