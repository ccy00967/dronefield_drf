from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (
    UserRegistrationView,
    UserLoginView,
    UserListView,
    UserDataUpdateView,
    CustomTokenObtainPairView,
)

urlpatterns = [
    path('token/obtain/', CustomTokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register', UserRegistrationView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('users', UserListView.as_view(), name='users'),
    path('userinfo/<pk>', UserDataUpdateView.as_view(), name='userdataupdate')
]