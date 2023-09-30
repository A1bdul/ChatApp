from django.db.models import Q
from django.shortcuts import render
from django.views import View

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import authentication, permissions
from App.models import ChatRoom, PrivateMessage, Group, GroupMessages
from App.serializers import ChatRoomSerializers, MessageSerializers, HomeFeedSerializers
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from user.models import User

from collections import namedtuple


@api_view(['GET', 'POST'])
def api_room_view(request):
    user = request.user
    rooms = ChatRoom.objects.filter(Q(user1=user) | Q(user2=user))
    instance = ChatRoomSerializers(rooms, many=True).data
    return Response(instance)



@api_view(['GET'])
def api_all_rooms(request):
    user = request.user
    all_rooms = namedtuple('RoomType', ['favourite_users', 'usersList', 'channelList'])
    rooms = all_rooms(
        favourite_users=[x for x in user.profile.favourite.all() if PrivateMessage.objects.filter(room=x)],
        usersList=[x for x in ChatRoom.objects.filter(Q(user1=user) | Q(user2=user))
                   if x not in user.profile.favourite.all()],
        channelList=Group.objects.filter(members__participant=user)
    )
    instance = HomeFeedSerializers(rooms, context={
        "request": request
    }).data

    return Response(instance)
