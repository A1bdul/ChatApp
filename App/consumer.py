import os
import threading
from typing import List, Any

import cloudinary
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from dotenv import load_dotenv
from App.models import ChatRoom, PrivateMessage, Group, Album, GroupMessages, Member
from user.models import User

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
                images.append(new_img['secure_url'])
                image = await database_sync_to_async(Album.objects.create)(images=new_img['secure_url'])
                await database_sync_to_async(self.msg.images.add)(image)
            except cloudinary.exceptions.Error:
                image = await database_sync_to_async(Album.objects.create)(images='/assets/images/small/img-1.jpg')
                await database_sync_to_async(self.msg.images.add)(image)
                images.append(image.images)
        return images


class ChatAppConsumer(AsyncJsonWebsocketConsumer):
    """

    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.me = None
        self.user2 = None
        self.chat_room = None
        self.room_name = None
        self.private = False
        self.msg = None

    async def connect(self):
        """ Handles connection with websocket """
        # checks if both users are authenticated then gets or create their chatroom

        self.me = self.scope['user']
        await self.accept()
        try:
            self.user2 = await database_sync_to_async(User.objects.get)(
                username=self.scope['url_route']['kwargs']['id'])
            self.private = True
        except User.DoesNotExist:
            self.chat_room = await database_sync_to_async(Group.objects.get)(id=self.scope['url_route']['kwargs']['id'])
        if self.private:
            self.chat_room = await database_sync_to_async(ChatRoom.get_room.get_or_create_room)(self.me, self.user2)
            self.room_name = f'private_room_{self.chat_room.id}'
            await database_sync_to_async(PrivateMessage.manage.read_all_message)(room=self.chat_room, user=self.me)
            await database_sync_to_async(self.chat_room.connected_users.add)(self.me)
        else:
            self.room_name = f'group_room_{str(self.chat_room.id)}'
            member = await database_sync_to_async(Member.objects.get)(participant=self.me)
            await database_sync_to_async(self.chat_room.connected_members.add)(member)
            await database_sync_to_async(GroupMessages.manage.read_group_message)(room=self.chat_room, user=self.me)

        await self.channel_layer.group_add(self.room_name, self.channel_name)

    def get_users(self):
        return self.chat_room.connected_users.all()

    async def receive_json(self, content, **kwargs):
        """ Handles all incoming message from websocket, each command is assigned to it own
            'type' function for execution
        """
        command = content.get('command')
        message = content.get('msg', '')
        if self.private:
            self.msg = PrivateMessage
            if command == 'typing':
                await self.channel_layer.group_send(self.room_name, {
                    'type': 'websocket_typing',  # Create a function with the name of the value in your type key
                    'user': self.scope['user']
                })
        else:
            self.msg = GroupMessages

        if content.get('images') or content.get('msg') or content.get('files'):
            if content.get('reply_id') is not None:
                # if this message is replying to a previous chat, assign reply to message in database
                reply = await database_sync_to_async(self.msg.objects.get)(id=content.get('reply_id'))
                new_msg = await database_sync_to_async(self.msg.objects.create)(room=self.chat_room, reply=reply,
                                                                                sender=self.me, msg=message)
                reply_from = await database_sync_to_async(User.objects.get)(username=content.get('reply_user'))
            else:
                new_msg = await database_sync_to_async(self.msg.objects.create)(room=self.chat_room,
                                                                                sender=self.me,
                                                                                msg=message)
                reply = None
                reply_from = None
            if self.private:
                if await database_sync_to_async(self.chat_room.get_if_connected_user)(self.user2):
                    await database_sync_to_async(PrivateMessage.manage.read_all_message)(room=self.chat_room,
                                                                                         user=self.user2)
                else:
                    await self.channel_layer.group_send(f'notification_to_{self.user2.username}', {
                        "type": "send_notification",
                        "private": self.private,
                        'user': self.me.username,
                        'count': await database_sync_to_async(PrivateMessage.manage.get_unread)(self.chat_room,
                                                                                                self.user2)
                    })
            else:
                for members in await database_sync_to_async(self.chat_room.get_not_connected_members)():
                    await self.channel_layer.group_send(f'notification_to_{members.participant.username}', {
                        "type": "send_notification",
                        "private": self.private,
                        "group": self.chat_room.id,
                        "count": await database_sync_to_async(GroupMessages.manage.get_group_unread)(self.chat_room,
                                                                                                     members.participant)
                    })
            data = {
                'type': 'websocket_private_chat',
                'text': new_msg.msg,
                'id': new_msg.id,
                "username": new_msg.sender.username,
                'first_name': new_msg.sender.first_name,
                "command": 'private_chat',
                "created_at": new_msg.created_at.strftime("%H:%M"),
                'images': [],
                'files': [],
                'dropdown': True
            }
            if content.get('reply_id') is not None:
                data['reply'] = reply
                data['reply_from'] = reply_from
            if content['images']:
                images = await CloudinaryUpload(content['images'], new_msg).start()
                data['images'] = images
                data['dropdown'] = False
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
            'dropdown': event['dropdown'],
            "created_at": event["created_at"],
            'reply': None,
            'read': await database_sync_to_async(self.chat_room.get_if_connected_user)(self.user2)
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

    async def disconnect(self, code):
        await database_sync_to_async(self.chat_room.connected_users.remove)(self.me)
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
