from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Chat(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller_chats")
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_chats")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.id}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")

    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:30]