# chat/consumers.py

import json
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message  

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json['message']

        # Get the user sending the message (you'll need user authentication)
        sender = self.scope["user"]

        # Create a new message and store it in the database
        message = Message.objects.create(
            content=message_text,
            sender=sender,
            recipient=None,  # You need to specify the recipient
            read_at=None  # Initial read status is None
        )

        # Send the message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_text,
                'sender_id': sender.id,
                'message_id': message.id
            }
        )

    async def chat_message(self, event):
        message_text = event['message']
        sender_id = event['sender_id']
        message_id = event['message_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message_text,
            'sender_id': sender_id,
            'message_id': message_id
        }))

        # Implement logic to handle read receipts
        await self.handle_read_receipt(sender_id, message_id)

    async def handle_read_receipt(self, sender_id, message_id):
        # Implement logic to update the read status of the message
        try:
            message = Message.objects.get(id=message_id)
            if message.recipient == self.scope["user"]:
                message.read_at = timezone.now()  # Update the read_at field
                message.save()
        except Message.DoesNotExist:
            pass  # Handle the case where the message doesn't exist

        # Send a read receipt to the sender
        await self.send(text_data=json.dumps({
            'read_receipt': True,
            'message_id': message_id
        }))
