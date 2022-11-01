from rest_framework import serializers
from MainApp.models import File
class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    timeFrame = serializers.IntegerField()
class SaveFileSerializer(serializers.Serializer):
    
    class Meta:
        model = File
        fields = "__all__"