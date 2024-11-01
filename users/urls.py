# users/urls.py
from django.urls import path
from .views import RegisterView, LoginView, LogoutView, UpdateProfileView, ProfileDetailView
from rest_framework_simplejwt.views import TokenRefreshView

# These contains url routes of the user APIs that would be accessed via frontend

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'), #
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # This is a backupp path, created in case in future, we want the frontend to refresh tokens before its expirty
    path('profile/update/', UpdateProfileView.as_view(), name='profile-update'),
    path('profile/', ProfileDetailView.as_view(), name='profile-detail')
]

