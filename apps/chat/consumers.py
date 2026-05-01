import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import UserChat, UserMessage


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        try:
            #GET CHAT ID
            self.chat_id = self.scope['url_route']['kwargs']['chat_id']
            self.room_group_name = f"chat_{self.chat_id}"

            #  GET USER
            self.user = self.scope.get("user")

            print("🔌 Trying to connect to chat:", self.chat_id)

            # CHECK MSFG
            chat_exists = await sync_to_async(
                UserChat.objects.filter(id=self.chat_id).exists
            )()

            if not chat_exists:
                print("❌ Chat NOT FOUND:", self.chat_id)
                await self.close()
                return

            #  JOIN GROUP
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
            print("✅ WebSocket CONNECTED:", self.chat_id)

        except Exception as e:
            print("❌ CONNECT ERROR:", e)
            await self.close()

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            print("❌ WebSocket DISCONNECTED")
        except Exception as e:
            print("❌ DISCONNECT ERROR:", e)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get("message")

            if not message:
                return

            # SENDER
            if self.user and not self.user.is_anonymous:
                sender = self.user.username
            else:
                sender = "guest"

            # SAVE TO DB
            await sync_to_async(UserMessage.objects.create)(
                chat_id=self.chat_id,
                text=message,
                sender_name=sender
            )

            #REALTIME SEND
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
        try:
            await self.send(text_data=json.dumps({
                "message": event["message"],
                "sender": event["sender"],
            }))
        except Exception as e:
            print("❌ SEND ERROR:", e)

    # 🔥 OPTIONAL: BOOKING NOTIFICATION
    # async def booking_update(self, event):
    #     try:
    #         await self.send(text_data=json.dumps({
    #             "type": "booking_update",
    #             "message": event["message"]
    #         }))
    #     except Exception as e:
    #         print("❌ BOOKING EVENT ERROR:", e)