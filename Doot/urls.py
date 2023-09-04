from django.contrib import admin
from django.urls import path, include
from djoser.views import TokenCreateView

urlpatterns = [
    path('', include('App.url')),
    path('', include('user.url')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
