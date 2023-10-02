from rest_framework import serializers
from user.serializers import UserInfoSerializer
from .models import ChatRoom, PrivateMessage, GroupMessages, Group, Member


# All User Information used will be serialized by the UserInfoSerializer,
# This is already defined to give only minimum info about the user needed

class ChatRoomSerializers(serializers.ModelSerializer):
    user2 = serializers.SerializerMethodField()
    unread = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = [
            'user2', 'id', 'unread'
        ]

    def get_unread(self, obj):
        try:
            user = self.context["request"]["user"]
        except TypeError:
            user = self.context["request"].user
        return PrivateMessage.manage.get_unread(obj, user)

    def get_user2(self, obj):
        try:
            user = self.context["request"]["user"]
        except TypeError:
            user = self.context["request"].user
        response = UserInfoSerializer(obj.user1, read_only=True)
        if obj.user1 == user:
            response = UserInfoSerializer(obj.user2, read_only=True)
        return response.data


class MemberSerializer(serializers.ModelSerializer):
    """
        Serialize group chat members information, will be used in other  class
        serializers
    """
    participant = UserInfoSerializer()

    class Meta:
        model = Member
        fields = [
            'participant', 'is_admin'
        ]


class GroupRoomSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, required=False)
    unread = serializers.SerializerMethodField(required=False)
    id = serializers.UUIDField(required=False)
    description = serializers.CharField()
    groupMembers = serializers.ListField(required=False)

    class Meta:
        model = Group
        fields = [
            'members', 'name', 'icon', 'id', 'unread', 'description', 'groupMembers'
        ]

    def create(self, validated_data):
        instance = Group.objects.create(name=validated_data.get("name"), description=validated_data.get("description"))
        for member in validated_data.get("groupMembers"):
            instance.members.add(member)
        return instance

    def get_unread(self, obj):
        if isinstance(obj, Group):
            try:
                user = self.context["request"]["user"]
            except TypeError:
                user = self.context["request"].user
            return GroupMessages.manage.get_group_unread(obj, user)


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


class MessageSerializers(serializers.Serializer):
    sender = UserInfoSerializer()
    msg = serializers.CharField()
    created_at = serializers.DateTimeField(format='%H:%M')
    dropdown = serializers.SerializerMethodField()
    images = AlbumSerializer(many=True, read_only=True)
    files = FileSerializer(many=True, read_only=True)
    id = serializers.IntegerField(read_only=True)
    read = serializers.SerializerMethodField()
    reply = MessageReplySerializer()

    class Meta:
        model = PrivateMessage
        fields = [
            'sender', 'id', 'msg', 'reply', 'created_at', 'images', 'files', 'dropdown'
        ]

    def get_read(self, obj):
        if isinstance(obj, PrivateMessage):
            user2 = obj.room.user1
            if obj.room.user1 == self.context["request"]["user"]:
                user2 = obj.room.user2
            return user2 in obj.read.all()

    def get_dropdown(self, obj):
        if isinstance(obj, PrivateMessage):
            if obj.images.all():
                return False
            return True
        return False


class HomeFeedSerializers(serializers.Serializer):
    favourite_users = ChatRoomSerializers(many=True)
    usersList = ChatRoomSerializers(many=True)
    channelList = GroupRoomSerializer(many=True)
