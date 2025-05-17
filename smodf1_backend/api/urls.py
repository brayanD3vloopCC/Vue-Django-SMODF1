from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ProjectImageViewSet, process_image

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'images', ProjectImageViewSet, basename='project-image')

urlpatterns = [
    path('', include(router.urls)),
    path('process_image/', process_image, name='process_image'),
    # URLs específicas para modelos 3D
    path('projects/<int:project_id>/models3d/', 
         ProjectViewSet.as_view({'get': 'get_3d_models'}), 
         name='project-3d-models'),
    path('projects/<int:project_id>/camera_capture/', 
         ProjectViewSet.as_view({'post': 'camera_capture'}), 
         name='project-camera-capture'),
    path('projects/<int:pk>/statistics/',
         ProjectViewSet.as_view({'get': 'get_statistics'}),
         name='project-statistics'),
] 