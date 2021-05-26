# DRF
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponse, Http404

# User
from django.contrib.auth.models import User

# File
from file.models import File
from file.serializers import FileSerializer

# path
import os

# django.core.exceptions.ImproperlyConfigured error
# from django.apps import AppConfig
# AppConfig.default = False

class FileViewSet(ModelViewSet):
    serializer_class = FileSerializer

    def get_queryset(self):
        return File.objects.all()

    # upload files
    def create(self, request, *args, **kwargs):
        # check user
        user = User.objects.filter(User.get_username(self))
        if user in User.objects.all():

            # upload files
            for file in request.FILES.getlist('files'):
                print('Upload', file)
                print('Upload', dir(file))

                f = File(file=file)
                f.save()

                f.file.name = os.path.join(user, f.file.name)
                print(f.file.path)

        return Response({'message': 'ok'}, status=status.HTTP_201_CREATED)


    # get each user's file list
    def list(self, request, *args, **kwargs):
        # check user
        user = User.objects.filter(User.get_username(self))
        if user in User.objects.all():

            # return file list
            print(request.FILES.getlist("files"))
            return super().list(request, args, kwargs)


    # download file
    # https://stackoverflow.com/questions/43441882/download-a-file-with-django
    def download(self, request):
        # check user
        user = User.objects.filter(User.get_username(self))
        if user in User.objects.all():

            # upload files
            files = []
            for file in request.FILES.getlist('files'):
                if file in File.objects.all():
                    print("Download", file)
                    print("Download", dir(file))
                    file = File(file=file)
                    files.append(file)
            return HttpResponse(files, content_type='text/plain')

        raise Http404
