import datetime

import boto3
from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from file.models import File
from file.serializers import FileSerializer
from django.http import FileResponse, QueryDict


class FileViewSet(ModelViewSet):
    serializer_class = FileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return File.objects.filter(user=self.request.user)

    # upload files
    def create(self, request, *args, **kwargs):
        new_data = request.data.dict()
        file_name = request.data['file_name']
        is_shared = request.data.get('is_shared', False)
        is_starred = request.data.get('is_starred', False)
        file = request.data['file']
        new_data['file_name'] = file_name
        new_data['is_shared'] = is_shared
        new_data['is_starred'] = is_starred
        new_data['file'] = file
        new_data['user'] = User.objects.get(username=self.request.user).id
        new_query_dict = QueryDict('', mutable=True)
        new_query_dict.update(new_data)
        file_serializer = FileSerializer(data=new_query_dict)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # get each user's file list
    # get query_set
    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


# 최근 문서함을 조회하는 api(구글 드라이브의 모든 문서가 수정된 날짜 순으로 조회됨을 볼 수 있다. -> 일정 기준 시간 이후에 수정된 파일을 조회)
class RecentFileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        now = datetime.datetime.now()
        compared_time = now - datetime.timedelta(days=2)
        file = File.objects.filter(user=self.request.user, modified_date__gte=compared_time)

        serializer = FileSerializer(file, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 중요 문서함을 조회하는 api
class StarredFileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        files = File.objects.filter(user=self.request.user, is_starred=True)

        serializer = FileSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DownloadViewSet(APIView):

    def get(self, request, file_name=""):
        s3 = boto3.client('s3')
        bucket_name = "storage.drive.jinsu.me"  # "mycloudcomputing-yeonsu"
        key_name = file_name

        # Generate the URL to get 'key-name' from 'bucket-name'
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': bucket_name,
                'Key': key_name
            }
        )

        # Use the URL to perform the GET operation. You can use any method you like
        # to send the GET, but we will use requests here to keep things simple.
        return Response(url, status=status.HTTP_200_OK)


class UpdateFileView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FileSerializer
    lookup_field = 'file_name'

    def get_queryset(self):
        return File.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else:
            return Response({"message": "failed", "details": serializer.errors})


class ShareFileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        files = File.objects.filter(is_shared=True)

        serializer = FileSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 파일 삭제 api
class DeleteFileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FileSerializer
    lookup_field = 'file_name'

    def get_queryset(self):
        return File.objects.filter(user=self.request.user)

    def delete(self, request, **kwargs):
        file_name = kwargs.get('file_name')
        file = File.objects.get(file_name=file_name)
        file.delete()
        return Response("Delete file {}".format(file_name), status=status.HTTP_200_OK)
