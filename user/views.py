from collections import defaultdict

from rest_framework.response import Response
from rest_framework.decorators import api_view
import string
from user.serializers import UserInfoSerializer, ProfileSerializer


# Create your views here.


@api_view(['GET', 'POST'])
def api_user(request):
    if request.user.is_authenticated:
        instance = UserInfoSerializer(request.user).data
        if request.method == 'POST':
            ser = ProfileSerializer(data=request.data)
            if ser.is_valid():
                request.user.profile.avatar = request.data['avatar']
                request.user.save()
            else:
                print(ser.errors)
        return Response(instance)


@api_view(['GET'])
def api_contacts(request):
    data = defaultdict(list)
    for i in string.ascii_uppercase:
        contacts = request.user.contacts.filter(first_name__startswith=i)
        for contact in contacts:
            data[i].append(UserInfoSerializer(contact).data)
    return Response(data)
