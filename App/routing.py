from django.urls import path
from .consumer import AppChatConsumer

websocket_patterns = [
    path('ws/<str:username>', AppChatConsumer.as_asgi())
]
