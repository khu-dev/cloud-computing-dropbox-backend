from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

# FileViewSet
from file.models import File
from file.serializers import FileSerializer

# PassthroughRenderer
from django.http import FileResponse
from rest_framework import viewsets, renderers
from rest_framework.decorators import action

# AssertionError: .accepted_media_type not set on Response
# https://stackoverflow.com/questions/55416471/how-to-resolve-assertionerror-accepted-renderer-not-set-on-response-in-django
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

# trashViewSet
from trash.models import Trash
from trash.serializers import TrashSerializer

# Return data as-is.
class PassthroughRenderer(renderers.BaseRenderer):
    serializer_class = FileSerializer
    media_type, format = '', ' '
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


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

    # Download file
    # https://stackoverflow.com/questions/38697529/how-to-return-generated-file-download-with-django-rest-framework
    @api_view(('GET',))                                         # resolve assertion error
    @renderer_classes((TemplateHTMLRenderer, JSONRenderer))     # resolve assertion error
    @action(methods=['get'], detail=True, renderer_classes=(PassthroughRenderer,))
    def download(self, *args, **kwargs):
        instance = self.get_object()

        # get an open file handle
        file_handle = instance.file.open()

        # send file
        response = FileResponse(file_handle, content_type='whatever')
        response['Content-Length'] = instance.file.size
        response['Content-Disposition'] = 'attachment; filename="%s"' % instance.file.name

        return response


    # move to trash
    def destroy(self, request, *args, **kwargs):
        
        # 삭제할 파일
        data = request.data
        file_serializer = FileSerializer(data=data)
        trash_serializer = TrashSerializer(data=data)

        # trash db에 추가
        if trash_serializer.is_valid():
            trash_serializer.save()

            # file db에서 삭제
            if file_serializer.is_valid():
                file_serializer.delete()
                return Response(trash_serializer.data, status=status.HTTP_301_MOVED_PERMANENTLY)

        else:
            return Response(trash_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
