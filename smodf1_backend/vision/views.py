from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import os

from .models import Project, ProjectImage
from .serializers import ProjectSerializer, ProjectImageSerializer
from .image_processing import extract_image_metadata, process_image_yolo, optimize_image

class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def upload_image(self, request):
        project_id = request.data.get('project_id')
        image_file = request.FILES.get('image')

        if not project_id or not image_file:
            return Response({'error': 'Missing project_id or image'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        try:
            project = Project.objects.get(id=project_id, user=request.user)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, 
                          status=status.HTTP_404_NOT_FOUND)


        # Guardar y optimizar imagen
        image_instance = ProjectImage.objects.create(
            project=project,
            image=image_file
        )

        # Ruta de la imagen
        image_path = os.path.join(settings.MEDIA_ROOT, str(image_instance.image))
        
        # Optimizar imagen
        optimized_path = image_path.replace('.', '_optimized.')
        optimize_image(image_path, optimized_path)
        
        # Extraer metadatos
        metadata = extract_image_metadata(image_path)
        
        # Procesar con YOLO
        yolo_results = process_image_yolo(
            image_path,
            settings.YOLO_WEIGHTS_PATH,
            settings.YOLO_CONFIG_PATH
        )
        
        # Actualizar resultados
        image_instance.metadata = metadata
        image_instance.analysis_results = yolo_results
        image_instance.processed = True
        image_instance.save()

        return Response({
            'message': 'Image uploaded and processed successfully',
            'image_id': image_instance.id,
            'metadata': metadata,
            'analysis': yolo_results
        })
