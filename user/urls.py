from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from user.views import RegisterView, ChangePasswordView, UpdateProfileView, UserListView

urlpatterns = [
    path('', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('login/refresh', TokenRefreshView.as_view()),
    path('login/verify', TokenVerifyView.as_view()),
    path('password/<int:pk>', ChangePasswordView.as_view()),
    path('profile/<int:pk>', UpdateProfileView.as_view()),
    path('list', UserListView.as_view()),
]