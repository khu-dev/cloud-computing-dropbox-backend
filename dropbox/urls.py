"""dropbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from file.views import FileViewSet, RecentFileView, StarredFileView, UpdateFileView, ShareFileView, DeleteFileView
from trash.views import TrashViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'files', FileViewSet, basename='files')
router.register(r'trash', TrashViewSet, basename='trash')

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', include(router.urls)),
    path('users/', include('user.urls')),
    path('', include('file.urls')),
    path('', include('trash.urls')),
    path('myfile/recent', RecentFileView.as_view()),
    path('myfile/starred', StarredFileView.as_view()),
    path('myfile/update/<str:file_name>', UpdateFileView.as_view()),
    path('myfile/share', ShareFileView.as_view()),
    path('myfile/delete/<str:file_name>', DeleteFileView.as_view()),
]
