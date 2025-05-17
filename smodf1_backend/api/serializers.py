from rest_framework import serializers
from .models import Project, ProjectImage

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'project', 'image', 'processed_image', 'uploaded_at', 'processed', 'analysis_results', 'has_3d_data', 'data_3d', 'image_width', 'image_height', 'file_size']
        read_only_fields = ['processed', 'processed_image', 'analysis_results', 'has_3d_data', 'data_3d', 'uploaded_at']

class ProjectSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'user', 'images']
        read_only_fields = ['created_at', 'updated_at', 'user'] 