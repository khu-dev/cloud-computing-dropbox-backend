from django.urls import path
from file.views import DownloadViewSet

urlpatterns = [
    path('<str:file_name>/download', DownloadViewSet.as_view()),
]