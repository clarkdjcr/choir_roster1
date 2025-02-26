import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage, ChoirMember
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.member_id = self.scope['url_route']['kwargs']['member_id']
        self.room_group_name = f'chat_{self.member_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.update_online_status(True)
        await self.notify_status_change(True)

    async def disconnect(self, close_code):
        await self.update_online_status(False)
        await self.notify_status_change(False)
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    @database_sync_to_async
    def get_choir_member(self, member_id):
        return ChoirMember.objects.get(id=member_id)

    @database_sync_to_async
    def save_message(self, sender, receiver, message):
        ChatMessage.objects.create(
            sender=sender,
            receiver=receiver,
            message=message
        )

    @database_sync_to_async
    def update_online_status(self, status):
        member = ChoirMember.objects.get(id=self.member_id)
        member.is_online = status
        member.save()

    async def notify_status_change(self, is_online):
        # Notify others about online status change
        await self.channel_layer.group_send(
            'status_updates',
            {
                'type': 'status_update',
                'member_id': self.member_id,
                'is_online': is_online
            }
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        receiver_id = data['receiver_id']

        receiver = await self.get_choir_member(receiver_id)
        sender = await self.get_choir_member(self.member_id)
        await self.save_message(sender, receiver, message)

        # Send to sender's group
        await self.channel_layer.group_send(
            f'chat_{self.member_id}',
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': self.member_id
            }
        )

        # Send to receiver's group
        await self.channel_layer.group_send(
            f'chat_{receiver_id}',
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': self.member_id,
                'sender_name': sender.user.get_full_name()
            }
        )

    async def chat_message(self, event):
        # Store unread message if recipient is offline
        if not await self.is_recipient_online(event['receiver_id']):
            await self.store_unread_message(event)
        
        await self.send(text_data=json.dumps(event)) 