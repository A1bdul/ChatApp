from rest_framework import serializers
from user.serializers import UserInfoSerializer
from .models import ChatRoom, PrivateMessage, GroupMessages, Group, Member


# All User Information used will be serialized by the UserInfoSerializer,
# This is already defined to give only minimum info about the user needed

class ChatRoomSerializers(serializers.ModelSerializer):
    user1 = UserInfoSerializer(read_only=True)
    user2 = UserInfoSerializer(read_only=True)
    unread = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = [
            'user1', 'user2', 'id', 'unread'
        ]

    def get_unread(self, obj):
        if isinstance(obj, ChatRoom):
            return {
                obj.user2.username: PrivateMessage.manage.get_unread(obj, obj.user2),
                obj.user1.username: PrivateMessage.manage.get_unread(obj, obj.user1)
            }


class MemberSerializer(serializers.ModelSerializer):
    """
        Serialize group chat members information, will be used in other  class
        serializers
    """
    participant = UserInfoSerializer(read_only=True)

    class Meta:
        model = Member
        fields = [
            'participant', 'is_admin'
        ]


class GroupRoomSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)
    messagecount = serializers.SerializerMethodField()
    id = serializers.UUIDField()
    memberscount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Group
        fields = [
            'members', 'name', 'icon', 'id', 'messagecount', 'memberscount'
        ]

    def get_messagecount(self, obj):
        if isinstance(obj, Group):
            data = {}
            for members in obj.members.all():
                data[members.participant.username] = GroupMessages.manage.get_group_unread(obj, members.participant)
            return data
    def get_memberscount(self, obj):
        return obj.members.count()


class AlbumSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.images


class FileSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.files


class MessageReplySerializer(serializers.ModelSerializer):
    sender = UserInfoSerializer(read_only=True)
    msg = serializers.CharField()

    class Meta:
        model = PrivateMessage
        fields = [
            'sender', 'id', 'msg'
        ]


class RoomMessageSerializers(serializers.Serializer):
    sender = UserInfoSerializer()
    msg = serializers.CharField()
    created_at = serializers.DateTimeField(format='%H:%M')
    dropdown = serializers.SerializerMethodField()
    images = AlbumSerializer(many=True, read_only=True)
    files = FileSerializer(many=True, read_only=True)
    id = serializers.IntegerField(read_only=True)
    reply = MessageReplySerializer()

    class Meta:
        model = PrivateMessage
        fields = [
            'sender', 'id', 'msg', 'reply', 'created_at', 'images', 'files', 'dropdown'
        ]

    def get_dropdown(self, obj):
        if obj.images.all():
            return False
        return True


class GroupMessageSerializer(serializers.Serializer):
    sender = UserInfoSerializer(read_only=True)
    msg = serializers.CharField()
    created_at = serializers.DateTimeField(format='%H:%M')
    dropdown = serializers.BooleanField(default=True)
    images = AlbumSerializer(many=True, read_only=True)
    files = FileSerializer(many=True, read_only=True)
    reply = MessageReplySerializer()
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = GroupMessages
        fields = [
            'sender', 'id', 'msg', 'reply', 'created_at', 'images', 'files', 'dropdown'
        ]


class HomeFeedSerializers(serializers.Serializer):
    favourite_users = ChatRoomSerializers(many=True)
    usersList = ChatRoomSerializers(many=True)
    channelList = GroupRoomSerializer(many=True)
