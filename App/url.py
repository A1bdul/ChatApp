from django.urls import path
from . import views


urlpatterns = [
    path('api-room-view/', views.api_room_view),
    path('api/all-room/', views.api_all_rooms)
]
