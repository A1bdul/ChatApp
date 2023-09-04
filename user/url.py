from django.urls import path
from . import views

urlpatterns = [
    path('user-api/', views.api_user),
    path('user-contacts/', views.api_contacts),
    path('auth/activate/<uid>/<token>', views.ActivateUser.as_view({'get':'activation'}, name='activation')),
]
