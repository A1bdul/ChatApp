from django.urls import path
from .consumer import AppChatConsumer, GroupChatConsumer

websocket_patterns = [
    path('ws/<str:username>', AppChatConsumer.as_asgi()),
    path('ws/group/<str:group_id>', GroupChatConsumer.as_asgi())
]
