from rest_framework import serializers
from user.serializers import UserLessInfoSerializer
from .models import ChatRoom, PrivateMessage, GroupMessages, Group, Member


# All User Information used will be serialized by the UserLessInfoSerializer,
# This is already defined to give only minimum info about the user needed

class ChatRoomSerializers(serializers.ModelSerializer):
    unread = serializers.SerializerMethodField(read_only=True)
    user1 = UserLessInfoSerializer(read_only=True)
    user2 = UserLessInfoSerializer(read_only=True)

    class Meta:
        model = ChatRoom
        fields = [
            'user1', 'user2', 'id', 'unread'
        ]

    def get_unread(self, obj):
        if isinstance(obj, ChatRoom):
            return PrivateMessage.objects.filter(room=obj, read=True).count()


class MemberSerializer(serializers.ModelSerializer):
    """
        Serialize group chat members information, will be used in other  class
        serializers
    """
    participant = UserLessInfoSerializer(read_only=True)

    class Meta:
        model = Member
        fields = [
            'participant', 'is_admin'
        ]


class GroupRoomSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)

    class Meta:
        model = Group
        fields = [
            'members', 'name', 'icon'
        ]


class AlbumSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.images


class FileSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.files


class RoomMessageSerializers(serializers.Serializer):
    sender = UserLessInfoSerializer(read_only=True)
    msg = serializers.CharField()
    created_at = serializers.DateTimeField(format='%H:%M')
    dropdown = serializers.BooleanField(default=True)
    images = AlbumSerializer(many=True, read_only=True)
    files = FileSerializer(many=True, read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = PrivateMessage
        fields = [
            'sender', 'id', 'msg', 'reply', 'created_at', 'images', 'files', 'dropdown'
        ]


class HomeFeedSerializers(serializers.Serializer):
    private_chat = ChatRoomSerializers(many=True)
    group_chat = GroupRoomSerializer(many=True)
