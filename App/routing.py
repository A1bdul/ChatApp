from django.urls import path
from .consumer import ChatAppConsumer
from notification.consumer import MyConsumer
"""
    assigning websocket url connection request to chat consumer class
    and handle message and send back information. 
"""

websocket_patterns = [
    path('ws/<str:id>', ChatAppConsumer.as_asgi()),
    path('ws/home/', MyConsumer.as_asgi())
]
