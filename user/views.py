from rest_framework.response import Response
from rest_framework.decorators import api_view

from user.serializers import UserFullInfoSerializers
# Create your views here.


@api_view(['GET'])
def api_user(request):
    if request.user.is_authenticated:
        instance = UserFullInfoSerializers(request.user).data
        return Response(instance)
