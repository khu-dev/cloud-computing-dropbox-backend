from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from django.core.files.storage import default_storage

from file.models import File
from file.serializers import FileSerializer


class FileViewSet(ModelViewSet):
    serializer_class = FileSerializer
    def get_queryset(self):
        return File.objects.all()
    def create(self, request, *args, **kwargs):
        # print(request.FILES)
        # file = request.FILES['files']
        # print('Upload', file)
        # print('Upload', dir(file))
        # for f = File(file=file)
        # f.save()
        for file in request.FILES.getlist('files'):
            print('Upload', file)
            print('Upload', dir(file))
            f = File(file=file)
            f.save()

        return Response({'message': 'ok'}, status=status.HTTP_201_CREATED)

