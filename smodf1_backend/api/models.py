from django.db import models
import os
from django.utils import timezone
from django.conf import settings
import json
import re

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects', null=True)
    
    def __str__(self):
        return self.name

def get_upload_path(instance, filename):
    """
    Generar path para la imagen: project_<id>/images/<filename>
    Asegurar que el directorio exista antes de guardar
    """
    # Obtener la extensión del archivo
    name, ext = os.path.splitext(filename)
    
    # Crear un nombre de archivo seguro con timestamp
    safe_name = f"project_{instance.project.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}_{re.sub(r'[^\w\-\.]', '_', name)}{ext}"
    
    # Crear el path completo
    path = os.path.join(f'project_{instance.project.id}', 'images', safe_name)
    
    # Asegurar que el directorio existe
    directory = os.path.join(settings.MEDIA_ROOT, f'project_{instance.project.id}', 'images')
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    return path

def get_processed_path(instance, filename):
    """
    Generar path para la imagen procesada: project_<id>/processed/<filename>
    Asegurar que el directorio exista antes de guardar
    """
    # Crear el path completo
    path = os.path.join(f'project_{instance.project.id}', 'processed', filename)
    
    # Asegurar que el directorio existe
    directory = os.path.join(settings.MEDIA_ROOT, f'project_{instance.project.id}', 'processed')
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    return path

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_path)
    processed_image = models.ImageField(upload_to=get_processed_path, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    processing_started = models.DateTimeField(null=True, blank=True)
    processing_completed = models.DateTimeField(null=True, blank=True)
    
    # Campos para resultados del análisis
    analysis_results = models.JSONField(null=True, blank=True)
    has_3d_data = models.BooleanField(default=False)
    data_3d = models.JSONField(null=True, blank=True)
    
    # Campos para metadatos
    image_width = models.IntegerField(null=True, blank=True)
    image_height = models.IntegerField(null=True, blank=True)
    file_size = models.IntegerField(null=True, blank=True)  # en bytes
    
    def __str__(self):
        return f"Image {self.id} for project {self.project.name}"

    def save(self, *args, **kwargs):
        if not self.id and not self.processing_started:
            self.processing_started = timezone.now()
        super().save(*args, **kwargs)

    def start_processing(self):
        self.processing_started = timezone.now()
        self.save()

    def complete_processing(self):
        self.processing_completed = timezone.now()
        self.processed = True
        self.save()

    class Meta:
        ordering = ['-uploaded_at']

class ProcessingOperation(models.Model):
    """Modelo para registrar operaciones de procesamiento de imágenes"""
    project_image = models.ForeignKey(ProjectImage, related_name='operations', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    algorithm = models.CharField(max_length=100)
    parameters = models.JSONField(default=dict)
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True, null=True)
    execution_time_ms = models.IntegerField(default=0)  # Tiempo en milisegundos
    
    def __str__(self):
        return f"{self.algorithm} on {self.project_image} at {self.timestamp}"
    
    @property
    def parameters_formatted(self):
        """Devuelve los parámetros en formato legible"""
        if not self.parameters:
            return "No parameters"
        return json.dumps(self.parameters, indent=2)
    
    class Meta:
        ordering = ['-timestamp']
