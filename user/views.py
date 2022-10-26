from collections import defaultdict
from django.shortcuts import render, redirect
from djoser.views import UserViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
import string
from user.serializers import UserInfoSerializer, ProfileSerializer
from rest_framework.status import HTTP_204_NO_CONTENT


# Create your views here.


@api_view(['GET', 'POST'])
def api_user(request):
    if request.user.is_authenticated:
        instance = UserInfoSerializer(request.user).data

        if request.method == 'POST':
            ser = ProfileSerializer(data=request.data)
            if ser.is_valid():
                request.user.profile.avatar = request.data['avatar']
                request.user.profile.save()
        return Response(instance)


@api_view(['GET'])
def api_contacts(request):
    data = defaultdict(list)
    for i in string.ascii_uppercase:
        contacts = request.user.contacts.filter(first_name__startswith=i)

        for contact in contacts:
            data[i].append(UserInfoSerializer(contact).data)
    return Response(data)


class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())

        kwargs['data'] = {'uid': self.kwargs['uid'], 'token': self.kwargs['token']}

        return serializer_class(*args, **kwargs)

    def activation(self, request, *args, **kwargs):
        super(ActivateUser, self).activation(request, *args, **kwargs)
        return Response(status=HTTP_204_NO_CONTENT)


def user_login(request, *args, **kwargs):
    return render(request, 'auth-login.html')


def user_register(request):
    return render(request, 'auth-register.html')

