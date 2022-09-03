from django.urls import path
from .consumer import AppChatConsumer, GroupChatConsumer
"""
    assigning websocket url connection request to chat consumer class
    and handle message and send back information. 
"""

websocket_patterns = [
    path('ws/<str:username>', AppChatConsumer.as_asgi()),
    path('ws/group/<str:group_id>', GroupChatConsumer.as_asgi())
]
