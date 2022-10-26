import os
from typing import List, Any

from dotenv import load_dotenv
import cloudinary
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from notification.models import Notification
from user.models import User
from App.models import ChatRoom, PrivateMessage, Group, Album, GroupMessages
import threading
from channels.db import database_sync_to_async

load_dotenv()

channels_sockets = []


async def disconnect_existing_sockets(sockets):
    if sockets:
        for socket in sockets:
            await socket.close()
    channels_sockets.clear()


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
            except cloudinary.exceptions.Error as e:
                image = await database_sync_to_async(Album.objects.create)(images='/assets/images/small/img-1.jpg')
                await database_sync_to_async(self.msg.images.add)(image)
                images.append(image.images)
        return images


class ChatAppConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.private = False

    async def connect(self):
        """ Handles connection with websocket """
        # checks if both users are authenticated then gets or create their chatroom
        self.me = self.scope['user']

        try:
            self.user2 = await database_sync_to_async(User.objects.get)(
                username=self.scope['url_route']['kwargs']['id'])
            self.private = True
        except User.DoesNotExist:
            self.chat_room = await database_sync_to_async(Group.objects.get)(id=self.scope['url_route']['kwargs']['id'])
        if self.private:
            self.chat_room = await database_sync_to_async(ChatRoom.get_room.get_or_create_room)(self.me, self.user2)
            self.room_name = f'private_room_{self.chat_room.id}'
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            await database_sync_to_async(PrivateMessage.manage.read_all_message)(room=self.chat_room, user=self.me)
            notifit = await database_sync_to_async(Notification.objects.filter)(to_user=self.me.id,
                                                                                from_user=self.user2.id)
            await database_sync_to_async(notifit.delete)()
        else:
            self.room_name = f'group_room_{str(self.chat_room.id)}'
            await self.channel_layer.group_add(self.room_name, self.channel_name)
            await database_sync_to_async(GroupMessages.manage.read_group_message)(room=self.chat_room, user=self.me)

        channels_sockets.append(self)

        await self.accept()

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
                await database_sync_to_async(Notification.objects.create)(from_user=self.me, to_user=self.user2)
            else:
                await database_sync_to_async(Notification.objects.create)(group=self.chat_room, from_user=self.me)

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

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)
