import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import datetime

from comment.models import Comment


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['task_id']
        self.room_group_name = 'chat_%s' % self.room_name

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

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        task_id = text_data_json['taskId']

        comment = await self.save_comment(message, task_id)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'comment_id': comment.id,
                'type': 'task_comment',
                'username': self.scope['user'].username,
                'datetime': datetime.datetime.now().strftime("%B %d, %Y, %I:%M %p"),
                'message': message
            }
        )

    # Receive message from room group
    async def task_comment(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'comment_id': event['comment_id'],
            'message': event['message'],
            'username': event['username'],
            'datetime': event['datetime'],
        }))

    @database_sync_to_async
    def save_comment(self, message, task_id):
        return Comment.objects.create(
            message=message,
            task_id=task_id,
            user_id=self.scope['user'].id,
        )
