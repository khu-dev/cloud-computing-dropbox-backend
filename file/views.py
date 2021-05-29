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

    # upload files
    def create(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

