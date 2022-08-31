from rest_framework import serializers
from user.serializers import UserLessInfoSerializer
from .models import ChatRoom, Messages


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
            return Messages.objects.filter(room=obj, read=True).count()


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
        model = Messages
        fields = [
            'sender', 'id', 'msg', 'reply', 'created_at', 'images', 'files', 'dropdown'
        ]
