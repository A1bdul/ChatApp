from channels.generic.websocket import AsyncJsonWebsocketConsumer

CONNECTIONS = set()


class MyConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.room = None

    async def connect(self):
        self.user = self.scope.get('user')
        await self.accept()
        self.room = f'notification_to_{self.user.id}'
        await self.channel_layer.group_add(self.room, self.channel_name)

    async def receive_json(self, content, **kwargs):
        command = content.get("command")
        if command == "messages_read":
            to = content.get("to")
            await self.channel_layer.group_send(f"notification_to_{to}", {
                "type": "read_messages",
                "user": self.user.id
            })

    async def chat_messages(self, event):
        await self.send({
            'chat_messages': True,
            "payload": event["data"]
        })

    async def read_messages(self, event):
        await self.send_json({
            "read": True,
            "user": event["user"]
        })

    async def send_notification(self, event):
        await self.send_json({
            "notification": True,
            "private": event["private"],
            "user": event["user"],
            "count": event["count"]
        })

    async def disconnect(self, code):
        CONNECTIONS.remove(self.user)
        await self.channel_layer.group_discard(self.room, self.channel_name)
