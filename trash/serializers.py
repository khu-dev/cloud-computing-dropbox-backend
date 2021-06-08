from rest_framework import serializers
from trash.models import Trash

class TrashSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trash
        fields = ('file_name', 'register_date', 'modified_date', 'is_shared', 'file', 'users')
