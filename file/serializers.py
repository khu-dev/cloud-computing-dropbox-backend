from rest_framework import serializers
from file.models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('file_name', 'register_date', 'modified_date', 'is_shared', 'is_starred', 'file', 'user')
