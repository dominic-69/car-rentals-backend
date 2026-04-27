from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


# =========================
# 🔥 USER ↔ USER CHAT
# =========================
class UserChat(models.Model):
    user1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="chat_user1"
    )
    user2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="chat_user2"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 🔥 prevent duplicate chats
        unique_together = ("user1", "user2")

    def __str__(self):
        return f"{self.user1} ↔ {self.user2}"


# =========================
# 🔥 MESSAGES
# =========================
class UserMessage(models.Model):
    chat = models.ForeignKey(
        UserChat,
        on_delete=models.CASCADE,
        related_name="messages"   # 🔥 IMPORTANT
    )

    text = models.TextField()

    # 🔥 SENDER (you are using username in frontend)
    sender_name = models.CharField(max_length=100)

    status = models.CharField(
        max_length=20,
        default="sent"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender_name}: {self.text[:30]}"