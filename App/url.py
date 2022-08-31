from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='index'),
    path('api-room-view', views.api_room_view),
    path('api/room-messages/<str:username>', views.api_room_messages)
]
