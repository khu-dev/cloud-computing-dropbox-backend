import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from django.core.files.storage import default_storage
from django.conf import settings
from django.http import HttpResponse, Http404

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


    # get each user's file list
    # get query_set
    def list(self, request, *args, **kwargs):
        print(request.FILES.getlist("file"))
        return super().list(request, args, kwargs)


class DownloadViewSet(ModelViewSet):
    serializer_class = FileSerializer

    def get_queryset(self):
        return File.objects.all()

    #########################################################################
    # download file
    # https://stackoverflow.com/questions/43441882/download-a-file-with-django
    # https://stackoverflow.com/questions/36392510/django-download-a-file
    def download(request, path):
        file_path = os.path.join(settings.MEDIA_ROOT, path)

        print("file path : ", file_path)

        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                print(response)
                return response
        raise Http404