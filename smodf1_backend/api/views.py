from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Project, ProjectImage, get_upload_path, get_processed_path
from .serializers import ProjectSerializer, ProjectImageSerializer
import os
from django.utils import timezone
from django.conf import settings
from vision.image_processor import ImageProcessor
import cv2
import numpy as np
import base64
import logging
import time

# Configurar logging
logger = logging.getLogger(__name__)

# Create your views here.

def process_image_internal(request_data, project_image_obj=None):
    """
    Función interna para procesar una imagen con algoritmos especificados.
    Puede ser llamada desde otras vistas para reutilizar el código.
    """
    
    image_id = request_data.get('image_id')
    pipeline = request_data.get('pipeline', [])
    
    if not pipeline:
        return {"error": "No processing pipeline specified"}
    
    # Variables para registrar operaciones
    start_time = timezone.now()
    operation_records = []
    
    try:
        # Get image from database if an ID was provided
        if image_id:
            try:
                if project_image_obj is None:
                    project_image_obj = ProjectImage.objects.get(id=image_id)
                
                image_path = project_image_obj.image.path
                print(f"Cargando imagen desde ruta: {image_path}")
                original_image = cv2.imread(image_path)
                
                if original_image is None:
                    print(f"Error: No se pudo cargar la imagen del path: {image_path}")
                    # Crear imagen demo si no se puede cargar
                    width, height = 640, 480
                    original_image = np.ones((height, width, 3), dtype=np.uint8) * 200
                    cv2.circle(original_image, (200, 200), 80, (0, 0, 255), -1)
                else:
                    print(f"Imagen cargada exitosamente: {original_image.shape}")
                    
                    # Actualizar metadatos de imagen si no están definidos
                    if not project_image_obj.image_width or not project_image_obj.image_height:
                        height, width = original_image.shape[:2]
                        project_image_obj.image_width = width
                        project_image_obj.image_height = height
                        project_image_obj.save(update_fields=['image_width', 'image_height'])
            except ProjectImage.DoesNotExist:
                return {"error": "Imagen no encontrada"}
            except Exception as e:
                return {"error": f"Error cargando imagen: {str(e)}"}
        else:
            return {"error": "No se proporcionó un ID de imagen"}
        
        # Process the image through the pipeline
        print("Inicializando procesador de imágenes...")
        processor = ImageProcessor()
        processed_image = original_image.copy()
        results = {
            "detections": [],
            "metrics": {
                "processing_time": 0.0,
                "detection_count": 0,
                "average_confidence": 0.0,
                "resolution": f"{processed_image.shape[1]}x{processed_image.shape[0]}"
            }
        }
        
        # Apply algorithms in the pipeline
        for algorithm in pipeline:
            algo_id = algorithm.get('algorithm')
            params = algorithm.get('params', {})
            
            print(f"Aplicando algoritmo: {algo_id} con parámetros: {params}")
            
            # Medir tiempo para esta operación
            op_start_time = timezone.now()
            
            # Aquí va la lógica para cada algoritmo (igual que en process_image view)
            if algo_id == 'object_detection':
                # Apply object detection
                confidence = params.get('confianza_mínima', 0.5)
                print(f"Detectando objetos con confianza mínima: {confidence}")
                results["detections"] = processor.detect_objects(processed_image, confidence)
                results["metrics"]["detection_count"] = len(results["detections"])
                
                if results["detections"]:
                    # Draw bounding boxes
                    for det in results["detections"]:
                        x, y, w, h = int(det["x"]), int(det["y"]), int(det["width"]), int(det["height"])
                        cv2.rectangle(processed_image, (x, y), (x+w, y+h), (0, 255, 0), 3)
                        
                        # Crear un fondo para el texto para mejor visibilidad
                        text = f"{det['class']}: {det['confidence']:.2f}"
                        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                        cv2.rectangle(processed_image, (x, y-text_size[1]-10), (x+text_size[0]+10, y), (0, 0, 0), -1)
                        
                        # Dibujar el texto sobre el fondo
                        cv2.putText(processed_image, text, 
                                   (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            elif algo_id == 'people_detection':
                # Apply people detection
                scale_factor = params.get('factor_escala', 1.05)
                min_neighbors = params.get('min_vecinos', 3)
                min_height = params.get('altura_minima', 100)
                
                # Obtener detecciones de personas
                people_detections = processor.detect_people(
                    processed_image, 
                    scale_factor=scale_factor,
                    min_neighbors=min_neighbors,
                    min_height=min_height
                )
                
                # Agregar a los resultados
                results["detections"] = people_detections
                results["metrics"]["detection_count"] = len(people_detections)
                
                # Dibujar las detecciones de personas
                if people_detections:
                    for det in people_detections:
                        x, y, w, h = int(det["x"]), int(det["y"]), int(det["width"]), int(det["height"])
                        cv2.rectangle(processed_image, (x, y), (x+w, y+h), (255, 0, 0), 3)
                        
                        # Crear un fondo para el texto
                        text = f"{det['class']}: {det['confidence']:.2f}"
                        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                        cv2.rectangle(processed_image, (x, y-text_size[1]-10), (x+text_size[0]+10, y), (0, 0, 0), -1)
                        
                        # Dibujar el texto
                        cv2.putText(processed_image, text, 
                                   (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 100, 0), 2)
            
            elif algo_id == 'yolo':
                # Apply YOLO object detection
                sensitivity = params.get('sensitivity', 0.5)
                detail_level = params.get('detail_level', 5)
                
                # Usar el detector de objetos pero con parámetros ajustados para YOLO
                results["detections"] = processor.detect_objects(
                    processed_image, 
                    confidence_threshold=sensitivity
                )
                results["metrics"]["detection_count"] = len(results["detections"])
                
                if results["detections"]:
                    # Draw bounding boxes
                    for det in results["detections"]:
                        x, y, w, h = int(det["x"]), int(det["y"]), int(det["width"]), int(det["height"])
                        cv2.rectangle(processed_image, (x, y), (x+w, y+h), (0, 200, 255), 3)
                        
                        # Crear un fondo para el texto para mejor visibilidad
                        text = f"{det['class']}: {det['confidence']:.2f}"
                        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                        cv2.rectangle(processed_image, (x, y-text_size[1]-10), (x+text_size[0]+10, y), (0, 0, 0), -1)
                        
                        # Dibujar el texto sobre el fondo
                        cv2.putText(processed_image, text, 
                                   (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)
            
            elif algo_id == 'edge_detection':
                # Apply edge detection
                method = params.get('método', 'canny')
                threshold1 = params.get('umbral_inferior', 100)
                threshold2 = params.get('umbral_superior', 200)
                
                if method == 'canny':
                    processed_image = cv2.Canny(processed_image, threshold1, threshold2)
                    # Convert back to 3 channels
                    processed_image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2BGR)
                elif method == 'sobel':
                    gray = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
                    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
                    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
                    processed_image = cv2.magnitude(sobelx, sobely)
                    processed_image = cv2.normalize(processed_image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
                    processed_image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2BGR)
            
            elif algo_id == 'segmentation':
                # Apply segmentation
                method = params.get('método', 'watershed')
                num_segments = params.get('número_de_segmentos', 5)
                
                if method == 'kmeans':
                    # Convert to RGB for processing
                    pixels = processed_image.reshape((-1, 3))
                    pixels = np.float32(pixels)
                    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
                    _, labels, centers = cv2.kmeans(pixels, num_segments, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
                    centers = np.uint8(centers)
                    segmented = centers[labels.flatten()]
                    processed_image = segmented.reshape(processed_image.shape)
            
            elif algo_id == 'contour':
                # Apply contour detection (similar to edge but keeps the original image)
                sensitivity = params.get('sensitivity', 0.5)
                detail_level = params.get('detail_level', 5)
                
                # Convert to grayscale
                gray = cv2.cvtColor(processed_image, cv2.COLOR_BGR2GRAY)
                
                # Apply blur and then Canny
                blurred = cv2.GaussianBlur(gray, (5, 5), 0)
                threshold1 = int(100 * sensitivity)
                threshold2 = int(200 * sensitivity)
                edges = cv2.Canny(blurred, threshold1, threshold2)
                
                # Find contours
                contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                # Filter contours by area if detail level is provided
                min_area = 1000 / detail_level  # Adjust area threshold based on detail level
                filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
                
                # Draw contours on the original image
                cv2.drawContours(processed_image, filtered_contours, -1, (0, 255, 0), 2)
                
                # Add contour data to results
                contour_data = []
                for contour in filtered_contours:
                    # Convert contour to list of points
                    points = []
                    for point in contour:
                        x, y = point[0]
                        points.append({"x": int(x), "y": int(y)})
                    contour_data.append(points)
                
                # Add to results
                results["contours"] = contour_data
                results["metrics"]["contour_count"] = len(filtered_contours)
                
                # Generar datos 3D automáticamente cuando se usa el algoritmo contour
                print("Generando modelo 3D a partir del contorno...")
                try:
                    if project_image_obj:
                        # Crear una nueva instancia del ImageProcessor
                        model_processor = ImageProcessor()
                        
                        # Configuración basada en los parámetros del contorno
                        model_settings = {
                            "polygons": 2000,
                            "color_mode": "color",
                            "detail_level": detail_level,
                            "sensitivity": sensitivity,
                            "extraction_method": "contour",
                            "extrusion_scale": 1.0
                        }
                        
                        # Generar datos 3D
                        model_3d = model_processor.generate_3d_data(
                            project_image_obj.image.path,
                            settings=model_settings
                        )
                        
                        # Actualizar los metadatos del proyecto
                        if isinstance(model_3d, dict) and not model_3d.get('error'):
                            project_image_obj.has_3d_data = True
                            project_image_obj.data_3d = model_3d
                            project_image_obj.save(update_fields=['has_3d_data', 'data_3d'])
                            print("Modelo 3D generado y guardado correctamente")
                except Exception as e:
                    print(f"Error generando modelo 3D: {str(e)}")
            
            # Registrar la operación si existe la imagen en la base de datos
            if project_image_obj:
                op_end_time = timezone.now()
                execution_time_ms = int((op_end_time - op_start_time).total_seconds() * 1000)
                
                # Crear registro de operación
                from .models import ProcessingOperation
                operation = ProcessingOperation(
                    project_image=project_image_obj,
                    algorithm=algo_id,
                    parameters=params,
                    execution_time_ms=execution_time_ms,
                    success=True
                )
                operation_records.append(operation)
        
        # Guardar los registros de operaciones en la base de datos
        from .models import ProcessingOperation
        if project_image_obj and operation_records:
            ProcessingOperation.objects.bulk_create(operation_records)
        
        # Convert processed image to base64 for response
        print("Convirtiendo imagen procesada a base64...")
        _, buffer = cv2.imencode('.jpg', processed_image)
        processed_image_base64 = "data:image/jpeg;base64," + base64.b64encode(buffer).decode('utf-8')
        
        # Update metrics
        if results["detections"]:
            confidences = [det.get("confidence", 0) for det in results["detections"]]
            results["metrics"]["average_confidence"] = sum(confidences) / len(confidences)
        
        # Guardar la imagen procesada si existe la imagen en la base de datos
        if project_image_obj:
            # Calcula tiempo total de procesamiento
            end_time = timezone.now()
            total_time_ms = (end_time - start_time).total_seconds() * 1000
            results["metrics"]["processing_time"] = total_time_ms
            
            try:
                # Guardar la imagen procesada en el sistema de archivos
                processed_filename = f"processed_{os.path.basename(project_image_obj.image.name)}"
                
                # Asegurar que el archivo tenga una extensión válida (.jpg)
                base, ext = os.path.splitext(processed_filename)
                if not ext or ext.lower() not in ['.jpg', '.jpeg', '.png']:
                    processed_filename = f"{base}.jpg"
                
                processed_path = os.path.join(settings.MEDIA_ROOT, get_processed_path(project_image_obj, processed_filename))
                
                # Asegurar que el directorio existe
                os.makedirs(os.path.dirname(processed_path), exist_ok=True)
                
                # Guardar imagen procesada con formato jpg
                cv2.imwrite(processed_path, processed_image)
                
                # Actualizar el objeto en la base de datos
                project_image_obj.processed_image.name = get_processed_path(project_image_obj, processed_filename)
                project_image_obj.analysis_results = results
                project_image_obj.processed = True
                project_image_obj.save()
                
                print(f"Imagen procesada guardada en: {processed_path}")
            except Exception as e:
                print(f"Error guardando imagen procesada: {str(e)}")
        
        # Imprimir un resumen de los resultados
        print(f"Procesamiento completado. Detecciones: {len(results['detections'])}")
        
        # Create response data
        response_data = {
            "processed_image": processed_image_base64,
            "results": results,
            "image_info": {
                "id": image_id,
                "name": project_image_obj.image.name if project_image_obj else "demo_image.jpg",
                "width": processed_image.shape[1],
                "height": processed_image.shape[0],
                "operations_performed": len(operation_records)
            } if project_image_obj else {
                "id": None,
                "name": "demo_image.jpg",
                "width": processed_image.shape[1],
                "height": processed_image.shape[0],
                "operations_performed": 0
            }
        }
        
        # Añadir datos del modelo 3D si existen
        if project_image_obj and project_image_obj.has_3d_data and project_image_obj.data_3d:
            print("Añadiendo modelo 3D existente a la respuesta")
            response_data["model_3d"] = project_image_obj.data_3d
        
        return response_data
        
    except Exception as e:
        import traceback
        print(f"Error procesando imagen: {str(e)}")
        print(traceback.format_exc())
        return {"error": str(e)}

@api_view(['POST', 'OPTIONS'])
def process_image(request):
    """
    Process an image with specified algorithms.
    The image can be provided as image_id or raw base64 data.
    """
    # Para solicitudes OPTIONS (preflight CORS)
    if request.method == 'OPTIONS':
        response = Response()
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
        return response
    
    # Información detallada sobre lo que se recibió
    print("=" * 50)
    print("SOLICITUD DE PROCESAMIENTO DE IMAGEN RECIBIDA")
    print(f"Tipo de solicitud: {request.method}")
    print(f"Content-Type: {request.content_type}")
    print("Headers:", request.headers)
    print(f"Datos de la solicitud: {request.data}")
    print("=" * 50)
    
    # Procesar la imagen utilizando la función interna
    result = process_image_internal(request.data)
    
    # Verificar si hay error
    if "error" in result:
        return Response({"error": result["error"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Generar modelo 3D si no está incluido en el resultado
    if "model_3d" not in result:
        print("Generando modelo 3D para la respuesta...")
        image_id = request.data.get('image_id')
        try:
            if image_id:
                # Obtener la imagen y generar modelo 3D
                project_image = ProjectImage.objects.get(id=image_id)
                
                # Usar el procesador de imágenes
                processor = ImageProcessor()
                
                # Extraer parámetros para el modelo 3D
                pipeline = request.data.get('pipeline', [])
                settings = {}
                
                # Extraer parámetros del pipeline
                for algo in pipeline:
                    if algo.get('algorithm') in ['contour', 'segmentation', 'yolo']:
                        settings = algo.get('params', {})
                        break
                
                # Generar datos 3D a partir de la imagen
                model_3d_data = processor.generate_3d_data(
                    project_image.image.path, 
                    settings=settings
                )
                
                if not isinstance(model_3d_data, dict) or not model_3d_data.get('error'):
                    # Añadir datos 3D al resultado
                    result["model_3d"] = model_3d_data
                    
                    # Actualizar la imagen con los datos 3D generados
                    project_image.has_3d_data = True
                    project_image.data_3d = model_3d_data
                    project_image.save()
                    
                    print("Modelo 3D generado y añadido a la respuesta")
                else:
                    print(f"Error generando modelo 3D: {model_3d_data.get('error')}")
            else:
                print("No se pudo generar modelo 3D: No se proporcionó ID de imagen")
        except Exception as e:
            print(f"Error generando modelo 3D: {str(e)}")
            # No devolver error, solo continuar sin el modelo 3D
    
    # Crear una respuesta con los headers CORS explícitos
    response = Response(result)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
    return response

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
    queryset = Project.objects.all()

    def get_queryset(self):
        return Project.objects.all()

    def perform_create(self, serializer):
        logger.info(f"Creando proyecto con datos: {serializer.validated_data}")
        try:
            # Guardar proyecto sin usuario
            serializer.save(user=None)
            logger.info("Proyecto creado exitosamente")
        except Exception as e:
            logger.error(f"Error al crear proyecto: {str(e)}")
            raise

    @action(detail=True, methods=['GET'])
    def get_statistics(self, request, pk=None):
        """
        Retorna estadísticas del proyecto
        """
        project = self.get_object()
        
        # Obtener todas las imágenes del proyecto
        images = ProjectImage.objects.filter(project=project)
        
        # Calcular estadísticas
        total_images = images.count()
        processed_images = images.filter(processed=True).count()
        pending_images = total_images - processed_images
        images_with_3d = images.filter(has_3d_data=True).count()
        
        # Calcular tiempos promedio si hay imágenes procesadas
        avg_processing_time = 0
        if processed_images > 0:
            processed_imgs = images.filter(processed=True)
            times = [img.processing_completed - img.processing_started 
                    for img in processed_imgs 
                    if img.processing_completed and img.processing_started]
            
            if times:
                avg_time_seconds = sum(time.total_seconds() for time in times) / len(times)
                avg_processing_time = round(avg_time_seconds, 2)
        
        # Devolver estadísticas
        statistics = {
            'total_images': total_images,
            'processed_images': processed_images,
            'pending_images': pending_images,
            'images_with_3d': images_with_3d,
            'avg_processing_time': avg_processing_time,
            'last_updated': project.updated_at
        }
        
        return Response(statistics)

    @action(detail=True, methods=['POST'])
    def upload_image(self, request, pk=None):
        project = self.get_object()
        image_file = request.FILES.get('image')
        
        if not image_file:
            return Response(
                {'error': 'No se proporcionó ninguna imagen'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Generar un nombre único para la imagen basado en timestamp y proyecto
            filename = f"project_{project.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}_{image_file.name}"
            
            # Crear la instancia de ProjectImage con el nombre único
            project_image = ProjectImage(project=project)
            project_image.image.save(filename, image_file)
            project_image.save()

            serializer = ProjectImageSerializer(project_image)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            if hasattr(project_image, 'image') and project_image.image:
                # Limpiar la imagen si hubo un error
                if os.path.exists(project_image.image.path):
                    os.remove(project_image.image.path)
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def generate_3d(self, request, pk=None):
        """
        Genera un modelo 3D a partir de una imagen existente en el proyecto
        """
        project = self.get_object()
        image_id = request.data.get('image_id')
        settings = request.data.get('settings', {})
        
        if not image_id:
            return Response({"error": "Se requiere un ID de imagen"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Obtener la imagen del proyecto
            project_image = ProjectImage.objects.get(id=image_id, project=project)
        except ProjectImage.DoesNotExist:
            return Response({"error": "Imagen no encontrada en este proyecto"}, status=status.HTTP_404_NOT_FOUND)
        
        # Usar el procesador de imágenes
        processor = ImageProcessor()
        
        # Generar datos 3D a partir de la imagen
        results = processor.generate_3d_data(
            project_image.image.path, 
            settings=settings
        )
        
        if isinstance(results, dict) and results.get('error'):
            return Response({"error": results['error']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Actualizar la imagen con los datos 3D generados
        project_image.has_3d_data = True
        project_image.data_3d = results
        project_image.save()
        
        return Response({
            "message": "Modelo 3D generado exitosamente",
            "results": results
        })

    @action(detail=True, methods=['post'])
    def update_3d_model(self, request, pk=None):
        """
        Actualiza los datos de un modelo 3D existente
        """
        project = self.get_object()
        image_id = request.data.get('image_id')
        model_data = request.data.get('model_data')
        settings = request.data.get('settings', {})
        
        if not image_id or not model_data:
            return Response({"error": "Se requiere ID de imagen y datos del modelo"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Obtener la imagen del proyecto
            project_image = ProjectImage.objects.get(id=image_id, project=project)
        except ProjectImage.DoesNotExist:
            return Response({"error": "Imagen no encontrada en este proyecto"}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        # Actualizar datos del modelo 3D
        project_image.has_3d_data = True
        project_image.data_3d = model_data
        
        # Guardar configuraciones actualizadas si se proporcionan
        if settings:
            if project_image.data_3d and isinstance(project_image.data_3d, dict):
                if 'metadata' in project_image.data_3d:
                    project_image.data_3d['metadata']['settings'] = settings
                else:
                    project_image.data_3d['metadata'] = {'settings': settings}
        
        project_image.save()
        
        return Response({
            "message": "Modelo 3D actualizado exitosamente",
            "model_id": image_id
        })

    @action(detail=True, methods=['get'])
    def get_3d_models(self, request, pk=None):
        """
        Obtiene todos los modelos 3D de un proyecto
        """
        project = self.get_object()
        
        # Obtener todas las imágenes con datos 3D
        models = ProjectImage.objects.filter(
            project=project,
            has_3d_data=True
        ).values('id', 'image', 'uploaded_at', 'data_3d')
        
        # Formatear la respuesta
        formatted_models = []
        for model in models:
            model_info = {
                'id': model['id'],
                'image_url': request.build_absolute_uri(model['image']),
                'created_at': model['uploaded_at'],
                'data_3d': model['data_3d']
            }
            
            # Extraer metadatos si están disponibles
            if model['data_3d'] and isinstance(model['data_3d'], dict) and 'metadata' in model['data_3d']:
                model_info['metadata'] = model['data_3d']['metadata']
            
            formatted_models.append(model_info)
        
        return Response(formatted_models)

    @action(detail=True, methods=['get'])
    def list_images(self, request, pk=None):
        """
        Lista todas las imágenes del proyecto con URLs absolutas
        """
        project = self.get_object()
        
        # Obtener todas las imágenes del proyecto
        images = ProjectImage.objects.filter(project=project)
        
        # Formatear la respuesta con URLs absolutas
        formatted_images = []
        for image in images:
            # Verificar si la imagen existe físicamente
            image_exists = False
            physical_path = None
            if image.image:
                physical_path = image.image.path
                image_exists = os.path.exists(physical_path)
            
            image_info = {
                'id': image.id,
                'name': f"Imagen {image.id}",
                'image': request.build_absolute_uri(image.image.url) if image.image else None,
                'uploaded_at': image.uploaded_at,
                'has_3d_data': image.has_3d_data,
                'file_exists': image_exists,
                'physical_path': physical_path,
            }
            
            formatted_images.append(image_info)
        
        return Response(formatted_images)

    @action(detail=True, methods=['post'])
    def camera_capture(self, request, pk=None):
        """
        Procesa una imagen capturada desde la cámara y opcionalmente genera un modelo 3D
        """
        project = self.get_object()
        
        # Validar la imagen
        if 'image' not in request.FILES:
            return Response({"error": "Se requiere una imagen"}, status=status.HTTP_400_BAD_REQUEST)
        
        image_file = request.FILES['image']
        generate_3d = request.data.get('generate_3d', False)
        settings = request.data.get('settings', {})
        
        # Crear la imagen en el proyecto
        project_image = ProjectImage.objects.create(
            project=project,
            image=image_file
        )
        
        # Extraer dimensiones de la imagen
        try:
            from PIL import Image
            with Image.open(project_image.image.path) as img:
                project_image.image_width, project_image.image_height = img.size
                project_image.file_size = os.path.getsize(project_image.image.path)
                project_image.save()
        except Exception as e:
            pass  # Continuar incluso si no se pueden extraer las dimensiones
        
        # Generar modelo 3D si se solicita
        if generate_3d:
            # Usar el procesador de imágenes
            processor = ImageProcessor()
            
            # Generar datos 3D
            results = processor.generate_3d_data(
                project_image.image.path, 
                settings=settings
            )
            
            if isinstance(results, dict) and not results.get('error'):
                project_image.has_3d_data = True
                project_image.data_3d = results
                project_image.save()
        
        # Serializar la respuesta
        serializer = ProjectImageSerializer(project_image)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def process_image(self, request, pk=None):
        """
        Procesa una imagen existente en el proyecto utilizando el proceso definido
        """
        project = self.get_object()
        image_id = request.data.get('image_id')
        
        if not image_id:
            return Response({"error": "ID de imagen no proporcionado"}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            # Obtener la imagen
            project_image = ProjectImage.objects.get(id=image_id, project=project)
            
            # Preparar los datos de la solicitud para el endpoint de procesamiento
            process_data = {
                'image_id': image_id,
                'pipeline': request.data.get('pipeline', [
                    {
                        'algorithm': 'edge_detection',
                        'params': {'método': 'canny', 'umbral_inferior': 100, 'umbral_superior': 200}
                    }
                ])
            }
            
            # Marcar la imagen como en procesamiento
            project_image.start_processing()
            
            # Realizar el procesamiento usando la función interna
            response_data = process_image_internal(process_data, project_image)
            
            # Verificar si hay error
            if "error" in response_data:
                return Response({"error": response_data["error"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
            return Response(response_data)
            
        except ProjectImage.DoesNotExist:
            return Response({"error": "Imagen no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Nuevo ViewSet para ProjectImage
class ProjectImageViewSet(viewsets.ModelViewSet):
    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImageSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Obtener el ID del proyecto
        project_id = request.data.get('project')
        
        try:
            # Verificar que el proyecto exista
            project = Project.objects.get(id=project_id)
            
            # Crear la imagen
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        except Project.DoesNotExist:
            return Response({"error": "Proyecto no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
