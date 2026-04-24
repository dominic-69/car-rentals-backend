from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async

from .models import UserChat, UserMessage


class UserChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = f"userchat_{self.chat_id}"

        # 🔥 Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print("✅ WebSocket Connected:", self.chat_id)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("❌ WebSocket Disconnected:", self.chat_id)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)

            message = data.get("message")
            sender = data.get("sender")

            # 🔥 VALIDATION
            if not message or not sender:
                return

            # 🔥 SAVE TO DB
            msg = await self.save_message(message, sender)

            # 🔥 SEND TO ROOM
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": msg.text,
                    "sender": msg.sender_name,
                    "message_id": msg.id,
                    "status": msg.status,
                }
            )

        except Exception as e:
            print("❌ ERROR:", str(e))

    async def chat_message(self, event):
        # 🔥 SEND TO FRONTEND
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
            "message_id": event["message_id"],
            "status": event["status"],
        }))

    # 🔥 DB SAVE FUNCTION
    @sync_to_async
    def save_message(self, message, sender):
        try:
            chat = UserChat.objects.get(id=self.chat_id)

            return UserMessage.objects.create(
                chat=chat,
                text=message,
                sender_name=sender,
                status="sent"
            )
        except UserChat.DoesNotExist:
            print("❌ Chat not found:", self.chat_id)
            return None