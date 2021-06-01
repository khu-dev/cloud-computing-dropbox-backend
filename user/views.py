from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import RegisterSerializer, UserSerializer, ChangePasswordSerializer, UpdateProfileSerializer


# 회원 가입
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# 사용자 조회 리스트
class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


# 비밀번호 변경 api
class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    lookup_field = "username"
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


# 사용자 프로필 업데이트 api
class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    lookup_field = "username"
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateProfileSerializer
