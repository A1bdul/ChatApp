from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from App.models import Member
from App.serializers import GroupRoomSerializer, MemberSerializer

CONNECTIONS = set()


class MyConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.room = None

    async def connect(self):
        self.user = self.scope.get('user')
        await self.accept()
        await sync_to_async(CONNECTIONS.add)(self.user)
        self.room = f'notification_to_{self.user.id}'
        await self.channel_layer.group_add(self.room, self.channel_name)

    async def receive_json(self, content, **kwargs) -> None:
        """
        This function receives a JSON payload and performs different actions based on the command given in the payload.

        Args:
            content (dict): The JSON payload.

        Returns:
            None
        """
        command = content.get("command")
        to = content.get("to")
        message = {
            "user": str(self.user.id)
        }

        if command == "messages_read":
            # If the command is "messages_read", send a group message to the specified channel.
            message["type"] = "messages_read"
            await self.channel_layer.group_send(f"notification_to_{to}", message)

        if command == "read_messages":
            # If the command is "read_messages", send a group message to the specified channel.
            message["type"] = "read_messages"
            await self.channel_layer.group_send(f"notification_to_{to}", message)

        if command == "channel_create":
            # If the command is "channel_create", create a new channel and send a group message to the user who
            # created the channel.
            data: dict = content.get("to")
            data["groupMembers"].append(str(self.user.id))
            data["groupMembers"] = await sync_to_async(self.serialize_members)(data["groupMembers"])
            instance = await sync_to_async(GroupRoomSerializer)(data=data)

            if await sync_to_async(instance.is_valid)():
                # If the instance is valid, save the channel and send a group message to the user who created the
                # channel.
                channel = await sync_to_async(instance.save)()
                await self.channel_layer.group_send(f"notification_to_{self.user.id}", {
                    "type": "channel_created",
                    "private": False,
                    "data": await sync_to_async(self.get_channel)(channel)
                })
            else:
                # If the instance is not valid, print the errors.
                print("invalid")
                print(instance.errors)

    async def channel_created(self, event):
        await self.send_json({
            event["type"]: True,
            "private": event["private"],
            "room": event["data"]
        })

    def serialize_members(self, members):
        group_members = []
        for user in members:
            member, created = Member.objects.get_or_create(participant_id=user)
            if member.participant.id == self.user.id:
                member.is_admin = True
            group_members.append(member)
        return group_members

    def get_channel(self, channel):
        return GroupRoomSerializer(channel, context={
            "request": self.scope
        }).data

    async def chat_messages(self, event):
        await self.send_json({
            'chat_messages': True,
            "payload": event["data"]
        })

    async def messages_read(self, event):
        await self.send_json({
            "read": True,
            "user": event["user"]
        })

    async def read_messages(self, event):
        print("sent")
        await self.send_json({
            "read_messages": True
        })

    async def send_notification(self, event):
        await self.send_json({
            "notification": True,
            "private": event["private"],
            "user": event["user"],
            "sender": event["sender"],
            "count": event["count"]
        })

    async def disconnect(self, code):
        CONNECTIONS.remove(self.user)
        await self.channel_layer.group_discard(self.room, self.channel_name)
