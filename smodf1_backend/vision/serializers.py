from rest_framework import serializers
from .models import Project, ProjectImage

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'uploaded_at', 'processed', 'metadata', 'analysis_results']
        read_only_fields = ['processed', 'metadata', 'analysis_results']

class ProjectSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, read_only=True)
    images_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'images', 'images_count']
        read_only_fields = ['created_at', 'updated_at']

    def get_images_count(self, obj):
        return obj.images.count() 