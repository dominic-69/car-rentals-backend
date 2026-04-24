from rest_framework import serializers
from .models import Chat, Message, UserChat, UserMessage


# =========================
# 🔥 OLD CHAT (SELLER ↔ ADMIN)
# =========================
class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.username", read_only=True)

    class Meta:
        model = Message
        fields = ["id", "text", "sender", "sender_name", "created_at"]


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ["id", "seller", "admin", "messages"]


# =========================
# 🔥 NEW CHAT (USER ↔ USER)
# =========================
class UserMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.username", read_only=True)

    class Meta:
        model = UserMessage
        fields = ["id", "text", "sender", "sender_name", "created_at"]


class UserChatSerializer(serializers.ModelSerializer):
    messages = UserMessageSerializer(many=True, read_only=True)

    user1_name = serializers.CharField(source="user1.username", read_only=True)
    user2_name = serializers.CharField(source="user2.username", read_only=True)

    class Meta:
        model = UserChat
        fields = [
            "id",
            "user1",
            "user1_name",
            "user2",
            "user2_name",
            "messages"
        ]