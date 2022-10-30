import uuid

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Q
from App.models import Group, GroupMessages, PrivateMessage

from user.models import User, ChatRoom


class MyConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):

        self.user = self.scope.get('user')
        await self.accept()
        self.me = self.user.username
        connected_users = await database_sync_to_async(ChatRoom.get_room.get_connected_users)(self.user)
        await database_sync_to_async(print)(connected_users)
        self.room = f'notification_to_{self.me}'
        await self.channel_layer.group_add(self.room, self.channel_name)
        for user in connected_users:
            await self.channel_layer.group_send(f'notification_to_{user}', {
                'type': 'send_status',
                'online': self.me
            })


    async def receive_json(self, content, **kwargs):
        from_user = content.get('home')
        try:
            group = await database_sync_to_async(Group.objects.get)(id=uuid.UUID(from_user))
            await database_sync_to_async(GroupMessages.manage.read_group_message)(room=group, user=self.user)
        except ValueError:
            user2 = await database_sync_to_async(User.objects.get)(username=from_user)
            room = await database_sync_to_async(ChatRoom.get_room.get_or_create_room)(self.user, user2)
            await database_sync_to_async(PrivateMessage.manage.read_all_message)(room=room, user=self.user)

    async def send_status(self, event):
        await self.send_json({'payload': event})

    async def websocket_notification(self, event):
        pass

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room, self.channel_name)
