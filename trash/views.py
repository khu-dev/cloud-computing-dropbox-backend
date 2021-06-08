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
        data = File.objects.get(file_name=file_name)

        # 휴지통 db에 삽입
        trash_data = Trash(
            file_name=data.file_name, register_date=data.register_date, modified_date=data.modified_date,
            is_shared=data.is_shared, file=data.file, users=data.user)
        trash_data.save()

        file = File.objects.get(file_name=file_name)
        file.delete()

        return Response("move to trash", status=status.HTTP_301_MOVED_PERMANENTLY)