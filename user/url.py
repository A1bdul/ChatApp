from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('user-api', views.api_user),
    path('auth', obtain_auth_token),
    path('user-error', views.api_contacts),
    path('auth/activate/<uid>/<token>', views.ActivateUser.as_view({'get':'activation'}, name='activation')),
    path('auth/login', views.user_login, name='login'),
    path('auth/register', views.user_register)
]