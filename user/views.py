from collections import defaultdict

from rest_framework.response import Response
from rest_framework.decorators import api_view
import string
from user.serializers import UserInfoSerializer

# Create your views here.


@api_view(['GET'])
def api_user(request):
    if request.user.is_authenticated:
        instance = UserInfoSerializer(request.user).data
        return Response(instance)


@api_view(['GET'])
def api_contacts(request):
    data = defaultdict(list)
    for i in string.ascii_uppercase:
        contacts = request.user.profile.contacts.filter(user__last_name__startswith=i)
        for user in contacts:
            data[i].append(UserInfoSerializer(user.user).data)
    return Response(data)
