from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('api-room-view', views.api_room_view),
    path('api/room-messages/<str:username>', views.api_room_messages),
    path('api/all-room', views.api_all_rooms),
    path('api/group-message/<str:group_id>', views.api_group_messages)
]
