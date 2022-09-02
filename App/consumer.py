from channels.generic.websocket import AsyncJsonWebsocketConsumer
from user.models import User
from App.models import ChatRoom, PrivateMessage, Group
from asgiref.sync import sync_to_async, async_to_sync


class AppChatConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.newmsg = None
        self.room_name = None
        self.me = None
        self.reply = None
        self.user2 = None
        self.chat_room = None

    async def connect(self):
        self.me = await sync_to_async(User.objects.get)(username=self.scope['user'])
        self.user2 = await sync_to_async(User.objects.get)(username=self.scope['url_route']['kwargs']['username'])
        await self.accept()
        self.chat_room = await sync_to_async(ChatRoom.get_room.get_or_create_room)(self.me, self.user2)
        self.room_name = f'private_room_{self.chat_room.id}'
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await sync_to_async(PrivateMessage.manage.read_all_message)(room=self.chat_room, user=self.me)

    async def receive_json(self, content, **kwargs):
        command = content.get('command')
        message = content.get('msg', None)

        if command == 'typing':
            await self.channel_layer.group_send(self.room_name, {
                'type': 'websocket_typing',
                'user': self.scope['user']
            })
        if command == 'private_chat':
            if content.get('reply_id'):
                self.reply = await sync_to_async(PrivateMessage.objects.get)(id=content.get('reply_id'))

                self.newmsg = await sync_to_async(PrivateMessage.objects.create)(room=self.chat_room, reply=self.reply,
                                                                                 sender=self.me,
                                                                                 msg=message)
                self.reply_from = await sync_to_async(User.objects.get)(username=content.get('reply_user'))
            else:
                self.newmsg = await sync_to_async(PrivateMessage.objects.create)(room=self.chat_room, sender=self.me,
                                                                                 msg=message)
            data = {
                'type': 'websocket_private_chat',
                'text': self.newmsg.msg,
                'id': self.newmsg.id,
                "username": self.newmsg.sender.username,
                'first_name': self.newmsg.sender.first_name,
                "command": command,
                "created_at": self.newmsg.created_at.strftime("%H:%M"),
            }
            if self.reply:
                data['reply'] = self.reply
                data['reply_from'] = self.reply_from
            await self.channel_layer.group_send(self.room_name, data)

    async def websocket_typing(self, event):
        await self.send_json({
            'type': 'typing',
            'user': event['user'].username
        })

    async def websocket_private_chat(self, event):
        message = {
            'sender': {
                "username": event["username"],
                "first_name": event['first_name']
            },
            'id': event["id"],
            'msg': event["text"],
            'command': event["command"],
            'images': [],
            'files': [],
            'dropdown': True,
            "created_at": event["created_at"],
            'reply': None
        }
        if self.reply:
            message['reply'] = {
                'id': event['reply'].id,
                'msg': event['reply'].msg,
                'sender': {
                    'username': event['reply_from'].username,
                    'first_name': event['reply_from'].first_name
                }
            }
        await self.send_json(message)


class GroupChatConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.group_id = None
        self.group = None
        self.group_room_name = None

    async def connect(self):
        await self.accept()

        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group = await sync_to_async(Group.objects.get)(id=self.group_id)
        self.group_room_name = f'{str(self.group.name).replace(" ", "")}-{str(self.group.id)}'

        await self.channel_layer.group_add(self.group_room_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        command = content.get('type', None)
        print(command)

