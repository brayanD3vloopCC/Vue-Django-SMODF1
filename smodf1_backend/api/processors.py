import os
import json
import numpy as np
import cv2
from PIL import Image
import logging
import math
from pathlib import Path
import time

# Configurar logging
logger = logging.getLogger(__name__)

class ImageProcessor:
    """
    Clase mejorada para procesar imágenes y generar datos 3D
    """
    
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png']
        # Crear directorios necesarios
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.models_dir = os.path.join(base_dir, 'models3d')
        
        # Crear directorios para los diferentes tipos de procesamiento
        self.specialized_dirs = {
            'personas': os.path.join(base_dir, 'opencv_personas'),
            'circuitos': os.path.join(base_dir, 'opencv_circuitos'),
            'trigonometria': os.path.join(base_dir, 'opencv_objetostrigonometria'),
            'rostros': os.path.join(base_dir, 'opencv_rostros'),
            'redondos': os.path.join(base_dir, 'opencv_objetos_redondos'),
        }
        
        # Asegurar que existan todos los directorios
        for directory in [self.models_dir] + list(self.specialized_dirs.values()):
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def process_image(self, image_path, settings=None):
        """
        Procesa una imagen y devuelve los resultados del análisis
        """
        if not settings:
            settings = {}
        
        try:
            # Verificar que la imagen existe
            if not os.path.exists(image_path):
                return {"error": "Imagen no encontrada"}
            
            # Cargar la imagen
            image = cv2.imread(image_path)
            if image is None:
                return {"error": "No se pudo cargar la imagen"}
            
            # Obtener dimensiones
            height, width, channels = image.shape
            
            # Análisis básico
            results = {
                "dimensions": {
                    "width": width,
                    "height": height,
                    "channels": channels
                },
                "format": os.path.splitext(image_path)[1],
                "size_kb": os.path.getsize(image_path) / 1024
            }
            
            # Análisis de color
            avg_color_per_row = np.average(image, axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)
            results["average_color"] = {
                "b": int(avg_color[0]),
                "g": int(avg_color[1]),
                "r": int(avg_color[2])
            }
            
            # Detección automática del tipo de imagen
            image_type = self._detect_image_type(image)
            results["detected_type"] = image_type
            
            return {
                "success": True,
                "analysis": results
            }
        except Exception as e:
            logger.error(f"Error procesando imagen: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _detect_image_type(self, image):
        """
        Detecta automáticamente el tipo de imagen basado en su contenido
        """
        # Convertir a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Usar diferentes detectores para identificar el tipo de contenido
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Detectar bordes
        edges = cv2.Canny(gray, 50, 200)
        edge_density = np.count_nonzero(edges) / (edges.shape[0] * edges.shape[1])
        
        # Detectar círculos
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1.2, minDist=100,
                                   param1=100, param2=30, minRadius=5, maxRadius=300)
        
        # Analizar resultados para determinar el tipo
        if len(faces) > 0:
            return "rostros"
        elif circles is not None and len(circles[0]) > 5:
            return "redondos"
        elif edge_density > 0.2:  # Muchos bordes indican posibles circuitos o figuras geométricas
            # Analizar si son patrones rectos (circuitos) o curvos (trigonometría)
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=80, minLineLength=50, maxLineGap=10)
            if lines is not None and len(lines) > 20:
                return "circuitos"
            else:
                return "trigonometria"
        else:
            # Analizar el histograma para personas
            hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
            hist_norm = hist / hist.sum()
            skin_range_sum = np.sum(hist_norm[70:150])  # Rango aproximado para tonos de piel
            if skin_range_sum > 0.4:
                return "personas"
        
        # Si no se puede determinar con certeza
        return "general"
    
    def generate_3d_data(self, image_path, settings=None):
        """
        Genera datos 3D a partir de una imagen usando algoritmos avanzados
        
        Args:
            image_path: Ruta a la imagen
            settings: Diccionario con configuraciones:
                - polygons: Número de polígonos (default: 2000)
                - color_mode: Modo de color ('color', 'grayscale', 'blueprint')
                - detail_level: Nivel de detalle (1-10)
                - sensitivity: Sensibilidad de extracción (0-1)
                - extraction_method: Método de extracción ('contour', 'segmentation', 'yolo')
                - extrusion_scale: Escala de extrusión para el modelo 3D
                
        Returns:
            Diccionario con datos 3D (vértices, caras, normales, colores)
        """
        if not settings:
            settings = {
                "polygons": 2000,
                "color_mode": "color",
                "detail_level": 5,
                "sensitivity": 0.5,
                "extraction_method": "contour",
                "extrusion_scale": 1.0
            }
        
        try:
            # Registrar inicio del procesamiento
            start_time = time.time()
            
            # Cargar la imagen
            image = cv2.imread(image_path)
            if image is None:
                return {"error": "No se pudo cargar la imagen"}
            
            # Determinar el tipo de imagen para procesamiento especializado
            image_type = self._detect_image_type(image)
            logger.info(f"Tipo de imagen detectado: {image_type}")
            
            # Aplicar método de extracción según configuración
            extraction_method = settings.get("extraction_method", "contour")
            detail_level = settings.get("detail_level", 5)
            sensitivity = settings.get("sensitivity", 0.5)
            
            # Convertir a escala de grises para el mapa de profundidad
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Variable para almacenar el mapa de profundidad
            depth_map = None
            
            # Aplicar método de extracción
            if extraction_method == "contour":
                depth_map = self._extract_depth_by_contours(gray, detail_level, sensitivity)
            elif extraction_method == "segmentation":
                depth_map = self._extract_depth_by_segmentation(image, gray, detail_level, sensitivity)
            elif extraction_method == "yolo":
                depth_map = self._extract_depth_by_object_detection(image, gray, detail_level, sensitivity)
            else:
                # Método por defecto
                depth_map = self._extract_depth_by_contours(gray, detail_level, sensitivity)
            
            # Aplicar filtros adicionales según el tipo de imagen
            if image_type == "rostros":
                depth_map = self._enhance_faces_depth_map(image, depth_map)
            elif image_type == "circuitos":
                depth_map = self._enhance_circuits_depth_map(image, depth_map)
            elif image_type == "redondos":
                depth_map = self._enhance_rounds_depth_map(image, depth_map)
            
            # Calcular resolución basada en número de polígonos deseados
            target_polygons = settings.get("polygons", 2000)
            scale_factor = max(1, int(np.sqrt((gray.shape[0] * gray.shape[1]) / (target_polygons * 2))))
            
            # Redimensionar mapa de profundidad
            resized_depth = cv2.resize(depth_map, 
                                      (gray.shape[1] // scale_factor, gray.shape[0] // scale_factor),
                                      interpolation=cv2.INTER_AREA)
            
            # Aplicar efecto según el modo de color seleccionado
            color_mode = settings.get("color_mode", "color")
            if color_mode == "grayscale":
                processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                processed_image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2BGR)
            elif color_mode == "blueprint":
                # Crea efecto blueprint (azul técnico)
                processed_image = np.zeros_like(image)
                processed_image[:,:,0] = 180  # Canal B (azul)
                processed_image[:,:,1] = 30 + gray // 4  # Canal G
                processed_image[:,:,2] = 5 + gray // 8   # Canal R
            else:  # color (normal)
                processed_image = image.copy()
            
            # Redimensionar la imagen procesada según el mapa de profundidad
            processed_image_resized = cv2.resize(processed_image, 
                                               (resized_depth.shape[1], resized_depth.shape[0]),
                                               interpolation=cv2.INTER_AREA)
            
            # Generar vertices, caras, normales y colores
            height, width = resized_depth.shape
            vertices = []
            faces = []
            normals = []
            colors = []
            
            # 1. Crear vértices
            for y in range(height):
                for x in range(width):
                    # Normalizar coordenadas entre -1 y 1
                    norm_x = (x / (width-1)) * 2 - 1
                    norm_y = -((y / (height-1)) * 2 - 1)  # Y invertido
                    
                    # Aplicar escala de extrusión
                    extrusion_scale = settings.get("extrusion_scale", 1.0)
                    norm_z = resized_depth[y, x] * extrusion_scale
                    
                    vertices.append([norm_x, norm_y, norm_z])
                    
                    # Normales - calcular gradiente del mapa de profundidad
                    if x > 0 and x < width-1 and y > 0 and y < height-1:
                        dx = resized_depth[y, x+1] - resized_depth[y, x-1]
                        dy = resized_depth[y+1, x] - resized_depth[y-1, x]
                        normal = [-dx, -dy, 1.0]  # Vector normal aproximado
                        length = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
                        if length > 0:
                            normal = [n/length for n in normal]
                        else:
                            normal = [0, 0, 1]
                    else:
                        normal = [0, 0, 1]  # Normal por defecto
                    
                    normals.append(normal)
                    
                    # Colores - extraer de la imagen procesada
                    b, g, r = [float(c)/255.0 for c in processed_image_resized[y, x]]
                    colors.append([r, g, b])  # RGB normalizado
            
            # 2. Crear caras (triángulos) - malla de triángulos
            for y in range(height - 1):
                for x in range(width - 1):
                    # Índices de los vértices para cada cuadrado de la malla
                    v0 = y * width + x
                    v1 = y * width + (x + 1)
                    v2 = (y + 1) * width + x
                    v3 = (y + 1) * width + (x + 1)
                    
                    # Crear dos triángulos por cada cuadrado
                    # Verificar que no haya cambios bruscos de profundidad (huecos en el modelo)
                    depth_threshold = 0.2
                    d0 = vertices[v0][2]
                    d1 = vertices[v1][2]
                    d2 = vertices[v2][2]
                    d3 = vertices[v3][2]
                    
                    # Solo crear caras si la diferencia de profundidad no es muy grande
                    if (abs(d0-d1) < depth_threshold and 
                        abs(d1-d3) < depth_threshold and 
                        abs(d3-d2) < depth_threshold and 
                        abs(d2-d0) < depth_threshold):
                        faces.append([v0, v1, v2])
                        faces.append([v1, v3, v2])
            
            # Generar el objeto 3D completo
            model_3d = {
                "vertices": vertices,
                "faces": faces,
                "normals": normals,
                "colors": colors,
                "metadata": {
                    "vertices_count": len(vertices),
                    "faces_count": len(faces),
                    "image_path": os.path.basename(image_path),
                    "image_type": image_type,
                    "processing_time": time.time() - start_time,
                    "settings": settings
                }
            }
            
            # Guardar el modelo 3D como archivo JSON
            model_filename = f"model3d_{Path(image_path).stem}_{image_type}.json"
            model_path = os.path.join(self.models_dir, model_filename)
            
            with open(model_path, 'w') as f:
                json.dump(model_3d, f)
            
            # Añadir ruta al resultado
            model_3d["file_path"] = model_path
            
            return model_3d
            
        except Exception as e:
            logger.error(f"Error generando datos 3D: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _extract_depth_by_contours(self, gray_image, detail_level, sensitivity):
        """
        Genera un mapa de profundidad basado en detección de contornos
        """
        # Ajustar parámetros según nivel de detalle y sensibilidad
        blur_size = max(1, 11 - detail_level)
        canny_low = int(150 * sensitivity)
        canny_high = int(250 * sensitivity)
        
        # Aplicar filtros para mejorar contraste y detección de bordes
        blurred = cv2.GaussianBlur(gray_image, (blur_size, blur_size), 0)
        edges = cv2.Canny(blurred, canny_low, canny_high)
        
        # Dilatar bordes para mejorar conexión
        kernel = np.ones((detail_level // 2 + 1, detail_level // 2 + 1), np.uint8)
        dilated_edges = cv2.dilate(edges, kernel, iterations=1)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(dilated_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Crear mapa de profundidad basado en contornos
        depth_map = gray_image.astype(np.float32) / 255.0
        
        # Dibujar contornos con diferentes profundidades
        contour_img = np.zeros_like(gray_image, dtype=np.float32)
        cv2.drawContours(contour_img, contours, -1, 1.0, thickness=detail_level)
        
        # Combinar mapa de profundidad base con contornos
        depth_map = depth_map * 0.7 + contour_img * 0.3
        
        # Suavizar el resultado
        depth_map = cv2.bilateralFilter(depth_map, 9, 75, 75)
        
        return depth_map
    
    def _extract_depth_by_segmentation(self, image, gray_image, detail_level, sensitivity):
        """
        Genera un mapa de profundidad basado en segmentación de la imagen
        """
        # Ajustar parámetros según nivel de detalle y sensibilidad
        num_segments = 50 + (detail_level * 20)
        sigma = 5.0 + (10 - detail_level)
        
        # Preprocesar la imagen
        blur = cv2.GaussianBlur(image, (5, 5), 0)
        
        # Aplicar algoritmo de segmentación Mean Shift
        # Parámetros: spatial radius, color radius, min size
        spatial_radius = int(10 + detail_level * 2)
        color_radius = int(10 + detail_level * 2)
        min_density = int(100 - detail_level * 8)
        
        segmented = cv2.pyrMeanShiftFiltering(blur, spatial_radius, color_radius, min_density)
        segmented_gray = cv2.cvtColor(segmented, cv2.COLOR_BGR2GRAY)
        
        # Aplicar umbral adaptativo para destacar regiones
        block_size = 11 + (10 - detail_level) * 2
        if block_size % 2 == 0:
            block_size += 1  # Debe ser impar
            
        threshold_value = 2 + int(sensitivity * 10)
        binary = cv2.adaptiveThreshold(segmented_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY, block_size, threshold_value)
        
        # Crear un mapa de profundidad basado en la segmentación
        depth_from_segmentation = binary.astype(np.float32) / 255.0
        
        # Combinar con el mapa de profundidad original
        depth_from_gray = gray_image.astype(np.float32) / 255.0
        
        # Combinar ambas fuentes
        alpha = 0.4 + sensitivity * 0.4  # Ajustar peso según sensibilidad
        depth_map = depth_from_gray * (1 - alpha) + depth_from_segmentation * alpha
        
        # Aplicar filtro bilateral para suavizar manteniendo bordes
        depth_map = cv2.bilateralFilter(depth_map, 9, 75, 75)
        
        return depth_map
    
    def _extract_depth_by_object_detection(self, image, gray_image, detail_level, sensitivity):
        """
        Genera un mapa de profundidad basado en detección de objetos
        """
        # Para simplificar, utilizaremos técnicas de computer vision tradicionales
        # En una implementación real, aquí se usaría un modelo YOLO o similar
        
        # Detector de bordes
        edges = cv2.Canny(gray_image, 50, 150)
        
        # Detector de características
        sift = cv2.SIFT_create(nfeatures=int(detail_level * 100))
        keypoints, _ = sift.detectAndCompute(gray_image, None)
        
        # Crear un mapa de densidad de características
        feature_map = np.zeros_like(gray_image, dtype=np.float32)
        
        # Dibujar puntos de interés con diferentes tamaños
        for kp in keypoints:
            x, y = int(kp.pt[0]), int(kp.pt[1])
            size = int(kp.size)
            if size < 1:
                size = 1
            cv2.circle(feature_map, (x, y), size, (255), -1)
        
        # Normalizar
        feature_map = feature_map / 255.0
        
        # Combinar con el mapa de profundidad basado en bordes
        depth_from_edges = edges.astype(np.float32) / 255.0
        
        # Crear un mapa de profundidad base desde la imagen en escala de grises
        depth_from_gray = gray_image.astype(np.float32) / 255.0
        
        # Combinar las tres fuentes con pesos según el nivel de detalle y sensibilidad
        w1 = 0.5 + (detail_level / 20)  # Peso para profundidad basada en grises
        w2 = 0.3 + (sensitivity * 0.3)  # Peso para bordes
        w3 = 0.2 + (detail_level / 20)  # Peso para características
        
        depth_map = (
            depth_from_gray * w1 +
            depth_from_edges * w2 +
            feature_map * w3
        ) / (w1 + w2 + w3)
        
        # Suavizar el resultado
        depth_map = cv2.bilateralFilter(depth_map, 9, 75, 75)
        
        return depth_map
    
    def _enhance_faces_depth_map(self, image, depth_map):
        """Mejora el mapa de profundidad para imágenes con rostros"""
        # Detectar rostros
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Crear una máscara para las regiones de rostros
        face_mask = np.zeros_like(depth_map)
        
        for (x, y, w, h) in faces:
            # Crear un gradiente radial para cada rostro
            center_x, center_y = x + w//2, y + h//2
            for i in range(y, y + h):
                for j in range(x, x + w):
                    # Calcular distancia normalizada al centro del rostro
                    dist = np.sqrt(((j - center_x) / (w/2))**2 + ((i - center_y) / (h/2))**2)
                    # Crear un abultamiento para el rostro (mayor en el centro)
                    if dist < 1.0:
                        boost = np.cos(dist * np.pi/2) * 0.5 + 0.5
                        face_mask[i, j] = boost
        
        # Combinar con el mapa de profundidad original
        enhanced_depth = depth_map * (1.0 - face_mask) + face_mask
        
        return enhanced_depth
    
    def _enhance_circuits_depth_map(self, image, depth_map):
        """Mejora el mapa de profundidad para imágenes con circuitos"""
        # Detectar líneas usando transformada de Hough
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 80, minLineLength=30, maxLineGap=10)
        
        # Crear una máscara para las líneas detectadas
        line_mask = np.zeros_like(depth_map)
        
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(line_mask, (x1, y1), (x2, y2), 1.0, 2)
        
        # Intensificar áreas de componentes electrónicos
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # Máscaras para colores comunes en componentes electrónicos
        mask_green = cv2.inRange(hsv, (35, 50, 50), (85, 255, 255))  # Verde (placas)
        mask_black = cv2.inRange(hsv, (0, 0, 0), (180, 255, 30))     # Negro (chips)
        
        component_mask = (mask_green + mask_black) / 255.0
        component_mask = cv2.dilate(component_mask, np.ones((5,5), np.uint8))
        
        # Combinar con el mapa de profundidad
        enhanced_depth = depth_map * 0.6 + line_mask * 0.2 + component_mask * 0.2
        
        return enhanced_depth
    
    def _enhance_rounds_depth_map(self, image, depth_map):
        """Mejora el mapa de profundidad para imágenes con objetos redondos"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detectar círculos
        circles = cv2.HoughCircles(
            gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
            param1=50, param2=30, minRadius=5, maxRadius=100
        )
        
        # Crear una máscara para destacar círculos
        circle_mask = np.zeros_like(depth_map)
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # Dibujar círculo con gradiente radial
                center = (i[0], i[1])
                radius = i[2]
                for y in range(max(0, center[1]-radius), min(depth_map.shape[0], center[1]+radius+1)):
                    for x in range(max(0, center[0]-radius), min(depth_map.shape[1], center[0]+radius+1)):
                        dist = np.sqrt((x - center[0])**2 + (y - center[1])**2)
                        if dist <= radius:
                            # Crear un abultamiento para el círculo
                            boost = np.cos(dist/radius * np.pi/2) * 0.5 + 0.5
                            circle_mask[y, x] = max(circle_mask[y, x], boost)
        
        # Combinar con el mapa de profundidad original
        enhanced_depth = depth_map * (1.0 - circle_mask * 0.7) + circle_mask * 0.7
        
        return enhanced_depth

    def apply_image_effect(self, image_path, effect, quality=80):
        """
        Aplica efectos visuales a una imagen
        """
        try:
            # Cargar imagen
            image = cv2.imread(image_path)
            if image is None:
                return {"error": "No se pudo cargar la imagen"}
            
            # Aplicar efecto
            if effect == "grayscale":
                processed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)
            elif effect == "blueprint":
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                processed = np.zeros_like(image)
                processed[:,:,0] = 180  # Canal B
                processed[:,:,1] = 30 + gray // 4  # Canal G
                processed[:,:,2] = 5 + gray // 8   # Canal R
            elif effect == "sepia":
                kernel = np.array([[0.272, 0.534, 0.131],
                                   [0.349, 0.686, 0.168],
                                   [0.393, 0.769, 0.189]])
                processed = cv2.transform(image, kernel)
            elif effect == "negative":
                processed = 255 - image
            elif effect == "cartoon":
                # Aplicar efecto de dibujo animado
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                gray = cv2.medianBlur(gray, 5)
                edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                             cv2.THRESH_BINARY, 9, 9)
                color = cv2.bilateralFilter(image, 9, 250, 250)
                processed = cv2.bitwise_and(color, color, mask=edges)
            elif effect == "emboss":
                kernel = np.array([[0,-1,-1],
                                   [1,0,-1],
                                   [1,1,0]])
                processed = cv2.filter2D(image, -1, kernel) + 128
            else:
                return {"error": f"Efecto no válido: {effect}"}
                
            # Guardar imagen procesada
            output_dir = os.path.dirname(image_path)
            output_filename = f"{Path(image_path).stem}_{effect}{Path(image_path).suffix}"
            output_path = os.path.join(output_dir, output_filename)
            
            # Guardar con compresión según calidad
            cv2.imwrite(output_path, processed, [cv2.IMWRITE_JPEG_QUALITY, quality])
            
            return {
                "success": True,
                "processed_path": output_path
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            } 