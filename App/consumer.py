from channels.generic.websocket import AsyncJsonWebsocketConsumer
from user.models import User
from App.models import ChatRoom, Messages
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
                self.reply = await sync_to_async(Messages.objects.get)(id=content.get('reply_id'), room=self.chat_room)
                self.newmsg = await sync_to_async(Messages.objects.create)(room=self.chat_room, sender=self.me, msg=message, reply=self.reply)
            else:
                self.newmsg = await sync_to_async(Messages.objects.create)(room=self.chat_room, sender=self.me,
                                                                           msg=message)
            data = {
                'type': 'websocket_private_chat',
                'text': self.newmsg.msg,
                'id': self.newmsg.id,
                "username": self.newmsg.sender.username,
                "command": command,
                "created_at": self.newmsg.created_at.strftime("%H:%M"),

            }
            if self.reply:
                data['reply'] = self.reply
                data['reply_username'] = self.reply.sender.username
            await self.channel_layer.group_send(self.room_name, data)

    async def websocket_typing(self, event):
        await self.send_json({
            'type': 'typing',
            'user': event['user'].username
        })

    async def websocket_private_chat(self, event):
        message = {
            'id': event["id"],
            'msg': event["text"],
            'command': event["command"],
            'sender': {
                "username": event["username"],
            },
            'images': [],
            'files': [],
            'dropdown': True,
            "created_at": event["created_at"]
        }
        if self.reply:
            message['reply'] = {
                'reply_msg': event['reply'].msg,
                'sender': event['reply'].sender.username
            }
        await self.send_json(message)

