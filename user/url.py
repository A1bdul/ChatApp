from django.urls import path
from . import views

urlpatterns = [
    path('user-api', views.api_user)
]