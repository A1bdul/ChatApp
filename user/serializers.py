from rest_framework import serializers
from .models import User


class UserLessInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'avatar', 'cover_image', 'about'
        ]


class UserFullInfoSerializers(serializers.ModelSerializer):
    contacts = UserLessInfoSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'contacts', 'email', 'about','avatar', 'cover_image', 'block_list'
        ]
