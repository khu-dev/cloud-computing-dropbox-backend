from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

# FileViewSet
from file.models import File
from file.serializers import FileSerializer

class TrashViewSet(ModelViewSet):
    serializer_class = FileSerializer

    def get_queryset(self):
        return File.objects.all()

    # create 함수 (휴지통에 파일을 저장한다)
    # def create(self, request, *args, **kwargs):