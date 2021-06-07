from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from file.models import File
from trash.models import Trash
from trash.serializers import TrashSerializer

# 휴지통 api
class TrashViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TrashSerializer

    def get_queryset(self):
        return Trash.objects.filter(users=self.request.user)

    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)

    def create(self, request, *args, **kwargs):

        # 휴지통으로 이동할 파일
        file_name = request.data["file_name"]
        del_data = request.data
        del_data["users"] = User.objects.get(username=self.request.user).id

        trash_serializer = self.get_serializer(data=del_data, many=isinstance(del_data, list))

        if trash_serializer.is_valid():
            # 휴지통 db에 삽입
            trash_serializer.save()

            # file db에서 삭제
            file = File.objects.get(file_name=file_name)
            file.delete()

            return Response(trash_serializer.data, status=status.HTTP_301_MOVED_PERMANENTLY)

        else:
            return Response(trash_serializer.errors, status=status.HTTP_400_BAD_REQUEST)