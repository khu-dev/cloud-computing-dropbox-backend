from django.urls import path
from trash.views import TrashViewSet

urlpatterns = [
    path('trash/list', TrashViewSet.list),
    path('trash', TrashViewSet.create),
]