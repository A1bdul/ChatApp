import os
from typing import List, Any
from dotenv import load_dotenv
import cloudinary
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from user.models import User
from App.models import ChatRoom, PrivateMessage, Group, Album, GroupMessages
from asgiref.sync import sync_to_async, async_to_sync
import threading

load_dotenv()


class CloudinaryUpload(threading.Thread):
    def __init__(self, data, msg):
        self.data = data
        self.msg = msg
        threading.Thread.__init__(self)

    async def start(self) -> List[Any]:
        cloudinary.config(
            cloud_name=os.getenv('cloud_name'),
            api_key=os.getenv('api_key'),
            api_secret=os.getenv('api_secret'),
            secure=os.getenv('secure')
        )
        images = []
        for img in self.data:
            try:
                new_img = cloudinary.uploader.upload(img)
                images.append(new_img.secure_url)
                image = await sync_to_async(Album.objects.create)(images=new_img.secure_url)
                await sync_to_async(self.msg.images.add)(image)
            except:
                image = await sync_to_async(Album.objects.create)(images='/assets/images/small/img-1.jpg')
                await sync_to_async(self.msg.images.add)(image)

        return images


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
        """ Handles connection with websocket """
        # checks if both users are authenticated then gets or create their chatroom
        self.me = await sync_to_async(User.objects.get)(username=self.scope['user'])
        self.user2 = await sync_to_async(User.objects.get)(username=self.scope['url_route']['kwargs']['username'])
        await self.accept()
        self.chat_room = await sync_to_async(ChatRoom.get_room.get_or_create_room)(self.me, self.user2)
        self.room_name = f'private_room_{self.chat_room.id}'
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await sync_to_async(PrivateMessage.manage.read_all_message)(room=self.chat_room, user=self.me)

    async def receive_json(self, content, **kwargs):
        """ Handles all incoming message from websocket, each command is assigned to it own
            'type' function for execution
        """
        command = content.get('command')
        message = content.get('msg', None)

        if command == 'typing':
            await self.channel_layer.group_send(self.room_name, {
                'type': 'websocket_typing',  # Create a function with the name of the value in your type key
                'user': self.scope['user']
            })
        if content.get('reply_id') is not None:
            # if this message is replying to a previous chat, assign reply to message in database
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
            "command": 'private_chat',
            "created_at": self.newmsg.created_at.strftime("%H:%M"),
            'images': [],
            'files': []
        }
        if content.get('reply_id') is not None:
            data['reply'] = self.reply
            data['reply_from'] = self.reply_from

        if command == 'private_chat':
            if content['images']:
                images = await CloudinaryUpload(content['images'], self.newmsg).start()
                data['images'] = images
            await self.channel_layer.group_send(self.room_name, data)

    async def websocket_typing(self, event):
        """ handles all websocket typing command """
        await self.send_json({
            # send back message to the websocket ...
            'type': 'typing',
            'user': event['user'].username
        })

    async def websocket_private_chat(self, event):
        """ Handles all private chat message incoming from websocket """
        message = {
            'sender': {
                "username": event["username"],
                "first_name": event['first_name'],
                "profile": {

                }
            },
            'id': event["id"],
            'msg': event["text"],
            'command': event["command"],
            'images': event['images'],
            'files': event['files'],
            'dropdown': True,
            "created_at": event["created_at"],
            'reply': None
        }
        if event.get('reply') is not None:
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
        self.me = self.scope['user']
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group = await sync_to_async(Group.objects.get)(id=self.group_id)
        self.group_room_name = f'{str(self.group.name).replace(" ", "")}-{str(self.group.id)}'
        await self.channel_layer.group_add(self.group_room_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        command = content.get('command', None)
        message = content.get('msg')
        if command == 'group_chat':
            group_msg = await sync_to_async(GroupMessages.objects.create)(room=self.group, msg=message, sender=self.me)
            await self.channel_layer.group_send(self.group_room_name, {
                'type': 'channel_chat',
                'sender': {
                    'username': self.me.username,
                    'first_name': self.me.first_name
                },
                'msg': message,
                'id': group_msg.id,
                "created_at": group_msg.created_at.strftime("%H:%M"),
                'images': [],
                'files': []
            })

    async def channel_chat(self, event):
        await self.send_json({
            'command': event['type'],
            'sender': {
                "username": event["sender"]['username'],
                "first_name": event['sender']['first_name'],
                "profile": {

                }
            },
            'id': event['id'],
            'msg': event['msg'],
            'images': event['images'],
            'files': event['files'],
            'dropdown': True,
            "created_at": event["created_at"],
            'reply': None
        })
