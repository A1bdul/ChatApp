from django.db.models import Q
from django.shortcuts import render

# Create your views here.
# class IndexView(View):
#     template_name = 'index.html'
#
#     def get(self, request):
#         return render(request, self.template_name)
from rest_framework.decorators import api_view
from rest_framework.response import Response

from App.models import ChatRoom, PrivateMessage, Group
from App.serializers import ChatRoomSerializers, RoomMessageSerializers, HomeFeedSerializers
from user.models import User
from collections import namedtuple


def home_view(request):
    return render(request, 'index.html')


@api_view(['GET'])
def api_room_view(request):
    user = request.user
    rooms = ChatRoom.objects.filter(Q(user1=user) | Q(user2=user))
    instance = ChatRoomSerializers(rooms, many=True).data
    return Response(instance)


@api_view(['GET'])
def api_room_messages(request, username):
    user2 = User.objects.get(username=username)
    room = ChatRoom.objects.filter(Q(user1=request.user, user2=user2) | Q(user2=request.user, user1=user2)).first()
    messages = PrivateMessage.manage.get_queryset(room)
    instance = RoomMessageSerializers(messages, many=True)
    return Response(instance.data)

@api_view(['GET'])
def api_all_rooms(request):
    user = request.user
    all_rooms = namedtuple('RoomType', ['private_chat', 'group_chat'])
    rooms = all_rooms(
        private_chat=ChatRoom.objects.filter(Q(user1=user) | Q(user2=user)), group_chat=Group.objects.filter(members__participant=user)
    )
    instance = HomeFeedSerializers(rooms, many=True).data
    return Response(instance)