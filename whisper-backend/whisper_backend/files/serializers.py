from rest_framework import serializers

from .models import Directory, File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = [
            "name",
            "size",
            "description",
            "processing_start",
            "processing_end",
            "processing_time",
            "status",
            "original_language",
            "original_text",
            "translated_text",
        ]


class DirectorySerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)
    subdirectories = serializers.SerializerMethodField()

    class Meta:
        model = Directory
        fields = ["name", "files", "subdirectories"]

    def get_subdirectories(self, obj):
        # Рекурсивно сериализуем поддиректории
        return DirectorySerializer(obj.subdirectories.all(), many=True).data
