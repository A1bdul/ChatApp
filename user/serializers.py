from rest_framework import serializers
from .models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'bio', 'avatar', 'cover_image', 'contacts', 'block_list'
        ]


class UserInfoSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'profile'
        ]

