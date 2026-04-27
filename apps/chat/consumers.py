import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import UserChat, UserMessage


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f"chat_{self.chat_id}"

        # 🔥 GET USER (may be anonymous)
        self.user = self.scope.get("user")

        # 🔥 CHECK CHAT EXISTS (IMPORTANT)
        try:
            await sync_to_async(UserChat.objects.get)(id=self.chat_id)
        except UserChat.DoesNotExist:
            await self.close()
            return

        # 🔥 JOIN ROOM (NO AUTH BLOCK FOR NOW)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print("✅ WebSocket CONNECTED:", self.user)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("❌ WebSocket DISCONNECTED")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get("message")

            # ❌ ignore empty
            if not message:
                return

            # 🔥 SAFE SENDER (IMPORTANT FIX)
            if self.user and not self.user.is_anonymous:
                sender = self.user.username
            else:
                sender = "guest"   # fallback (prevents crash)

            # 🔥 SAVE MESSAGE
            await UserMessage.objects.acreate(
                chat_id=self.chat_id,
                text=message,
                sender_name=sender
            )

            # 🔥 REALTIME BROADCAST
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sender": sender,
                }
            )

        except Exception as e:
            print("❌ RECEIVE ERROR:", e)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
        }))
        
# =========================
# 🔥 BOOKING UPDATE HANDLER
# =========================
async def booking_update(self, event):
    await self.send(text_data=json.dumps({
        "type": "booking_update",
        "message": event["message"]
    }))