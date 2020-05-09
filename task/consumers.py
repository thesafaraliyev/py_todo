import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from comment.models import Comment
from .models import Task, TaskUser


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
        # todo: validation needed

        user = self.scope['user']
        task_id = text_data_json['taskId']
        comment_id = text_data_json['identifier']
        action_type = text_data_json['actionType']

        context = {
            'state': True,
            'user_id': user.id,
            'username': user.username,
            'action_type': action_type,
            'type': 'task_comment',
        }

        try:
            if action_type == 'delete':
                await self.delete_comment(comment_id, user, task_id)
                context.update({
                    'comment_id': comment_id,
                })

            else:
                message = text_data_json['message']

                if action_type == 'update':
                    comment = await self.update_comment(comment_id, user, task_id, message)
                else:
                    comment = await self.create_comment(user, task_id, message)

                context.update({
                    'comment_id': comment.id,
                    'datetime': comment.created_at.strftime("%B %d, %Y, %I:%M %p"),
                    'message': message,
                })

        except (TaskUser.DoesNotExist, Task.DoesNotExist, Comment.DoesNotExist) as e:
            context.update({
                'state': False,
                'message': 'Something went wrong.',
            })
        finally:
            await self.channel_layer.group_send(self.room_group_name, context)

    async def task_comment(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def create_comment(self, user, task_id, message):
        task = Task.objects.get(pk=task_id)

        if not Task.objects.filter(author=user, pk=task.id).exists():
            TaskUser.objects.get(task=task, user=user, access_type=TaskUser.COMMENT)

        return Comment.objects.create(
            message=message,
            task_id=task.id,
            user_id=user.id,
        )

    @database_sync_to_async
    def update_comment(self, comment_id, user, task_id, message):
        task = Task.objects.get(pk=task_id)
        comment = Comment.objects.get(pk=comment_id, user_id=user.id)

        if not Task.objects.filter(author=user, pk=task.id).exists():
            TaskUser.objects.get(task=task, user=user, access_type=TaskUser.COMMENT)

        comment.message = message
        comment.save()
        return comment

    @database_sync_to_async
    def delete_comment(self, comment_id, user, task_id):
        comment = Comment.objects.get(id=comment_id)
        if Task.objects.filter(author=user, pk=task_id).exists() or Comment.objects.get(pk=comment_id, user_id=user.id):
            comment.delete()
        return comment_id
