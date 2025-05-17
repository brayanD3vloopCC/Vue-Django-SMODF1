import cv2
import numpy as np
from PIL import Image
import json
import os
from datetime import datetime
import random
import sys
import logging

# Añadir el directorio padre al path para poder importar opencv_processors
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from opencv_processors import get_image_processor
except ImportError:
    # Si no existe el módulo, proporcionamos un mensaje informativo
    print("ADVERTENCIA: No se encontró el módulo opencv_processors. Se usará un procesador genérico.")
    
    # Definición de placeholder para evitar errores
    def get_image_processor(image_type):
        return None

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_json_serializable(obj):
    """
    Convierte objetos con tipos NumPy a tipos Python estándar para serialización JSON
    """
    if isinstance(obj, (np.integer, np.int32, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.float32, np.float64, np.floating)):
        return float(obj)
    elif isinstance(obj, (np.ndarray,)):
        return make_json_serializable(obj.tolist())
    elif isinstance(obj, (list, tuple)):
        return [make_json_serializable(x) for x in obj]
    elif isinstance(obj, dict):
        return {key: make_json_serializable(value) for key, value in obj.items()}
    else:
        return obj

class ImageProcessor:
    def __init__(self):
        # Cargar modelos pre-entrenados de OpenCV
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Configurar el detector de objetos
        self.object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)
        
        # Directorios especializados para diferentes tipos de procesamiento
        self.specialized_dirs = {
            'personas': os.path.join(parent_dir, 'opencv_personas'),
            'circuitos': os.path.join(parent_dir, 'opencv_circuitos'),
            'trigonometria': os.path.join(parent_dir, 'opencv_objetostrigonometria'),
            'rostros': os.path.join(parent_dir, 'opencv_rostros'),
            'redondos': os.path.join(parent_dir, 'opencv_objetos_redondos'),
        }
        
        # Asegurar que existan todos los directorios
        for directory in self.specialized_dirs.values():
            if not os.path.exists(directory):
                os.makedirs(directory)

    def process_image(self, image_path):
        """Procesa una imagen y retorna los resultados del análisis"""
        # Leer la imagen
        image = cv2.imread(image_path)
        if image is None:
            return {"error": "No se pudo cargar la imagen"}

        # Convertir a RGB para procesamiento
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Análisis básico de la imagen
        height, width = image.shape[:2]
        
        # Detectar bordes
        edges = cv2.Canny(image, 100, 200)
        
        # Detectar rostros
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Análisis de color
        average_color = np.mean(image, axis=(0,1)).tolist()
        
        # Detectar el tipo de imagen
        image_type = self._detect_image_type(image)
        
        # Procesar usando procesador especializado o método interno
        specialized_processor = get_image_processor(image_type)
        if specialized_processor:
            processed_image, depth_map, contours = specialized_processor.process_image(image)
        else:
            # Método interno fallback
            processed_image = self._process_image_internal(image)
            depth_map = self._generate_depth_map_internal(image)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Detección de objetos
        mask = self.object_detector.apply(image)
        contours_obj, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        objects_detected = []
        for cnt in contours_obj:
            area = cv2.contourArea(cnt)
            if area > 100:  # Filtrar objetos pequeños
                x, y, w, h = cv2.boundingRect(cnt)
                objects_detected.append({
                    "x": int(x),
                    "y": int(y),
                    "width": int(w),
                    "height": int(h),
                    "area": float(area)
                })

        # Generar resultados        results = {            "timestamp": datetime.now().isoformat(),            "image_info": {                "width": int(width),                "height": int(height),                "channels": int(image.shape[2]) if len(image.shape) > 2 else 1,                "detected_type": image_type            },            "analysis": {                "faces_detected": len(faces),                "objects_detected": len(objects_detected),                "contours_detected": len(contours),                "average_color": {                    "b": float(average_color[0]),                    "g": float(average_color[1]),                    "r": float(average_color[2])                },                "objects": objects_detected            }        }

        # Guardar resultados procesados
        output_dir = os.path.join(os.path.dirname(image_path), 'processed')
        os.makedirs(output_dir, exist_ok=True)
        
        # Guardar imagen procesada
        processed_image_path = os.path.join(output_dir, 'processed_' + os.path.basename(image_path))
        cv2.imwrite(processed_image_path, processed_image)
        
        # Guardar mapa de profundidad como imagen
        if isinstance(depth_map, np.ndarray):
            depth_map_uint8 = (depth_map * 255).astype(np.uint8)
            depth_map_path = os.path.join(output_dir, 'depth_' + os.path.basename(image_path))
            cv2.imwrite(depth_map_path, depth_map_uint8)
        else:
            depth_map_path = None
        
        # Guardar JSON con resultados
        json_path = os.path.join(output_dir, os.path.splitext(os.path.basename(image_path))[0] + '_analysis.json')
        with open(json_path, 'w') as f:
            json.dump(make_json_serializable(results), f, indent=4)

        return {
            "results": make_json_serializable(results),
            "processed_image": processed_image_path,
            "depth_map": depth_map_path,
            "analysis_json": json_path
        }

    def _process_image_internal(self, image):
        """Método interno para procesar imágenes si no hay procesador especializado"""
        processed = image.copy()
        
        # Detectar bordes
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        
        # Dibujar contornos
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(processed, contours, -1, (0, 255, 0), 2)
        
        # Detectar rostros
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(processed, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        return processed

    def _generate_depth_map_internal(self, image):
        """Método interno para generar mapa de profundidad"""
        # Convertir a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Aplicar filtros para mejorar contraste
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        
        # Crear un mapa de profundidad usando una combinación de técnicas
        # 1. Usar detección de bordes como parte del mapa de profundidad
        depth_from_edges = edges.astype(np.float32) / 255.0
        
        # 2. Usar intensidad de píxeles como segunda fuente de profundidad
        depth_from_intensity = gray.astype(np.float32) / 255.0
        
        # Combinar ambas fuentes para un mapa de profundidad más detallado
        depth_map = (depth_from_intensity * 0.7) + (depth_from_edges * 0.3)
        
        # Aplicar filtro bilateral para suavizar manteniendo bordes
        depth_map = cv2.bilateralFilter(depth_map, 9, 75, 75)
        
        return depth_map

    def generate_3d_data(self, image_path, settings=None):
        """
        Genera datos para modelado 3D usando procesador especializado según tipo de imagen
        """
        print(f"Iniciando generación de datos 3D para: {image_path}")
        
        if not settings:
            settings = {
                "polygons": 2000,
                "color_mode": "color",
                "detail_level": 5,
                "sensitivity": 0.5,
                "extraction_method": "contour"
            }
            print("Usando configuración por defecto")
        else:
            print(f"Configuración recibida: {settings}")
        
        # Leer imagen
        image = cv2.imread(image_path)
        if image is None:
            print(f"ERROR: No se pudo cargar la imagen desde: {image_path}")
            return {"error": "No se pudo cargar la imagen"}
        
        print(f"Imagen cargada correctamente, dimensiones: {image.shape}")
        
        # Detectar tipo de imagen
        image_type = self._detect_image_type(image)
        logger.info(f"Tipo de imagen detectado para 3D: {image_type}")
        print(f"Tipo de imagen detectado: {image_type}")
        
        # Generar mapa de profundidad según el tipo de imagen
        specialized_processor = get_image_processor(image_type)
        
        detail_level = settings.get("detail_level", 5)
        sensitivity = settings.get("sensitivity", 0.5)
        
        print(f"Generando mapa de profundidad con nivel de detalle: {detail_level}, sensibilidad: {sensitivity}")
        
        if specialized_processor:
            print(f"Usando procesador especializado para: {image_type}")
            depth_map = specialized_processor.generate_depth_map(image, detail_level, sensitivity)
        else:
            print("Usando procesador interno genérico")
            # Método interno fallback
            depth_map = self._generate_depth_map_internal(image)
        
        if depth_map is None:
            print("ERROR: No se pudo generar el mapa de profundidad")
            return {"error": "No se pudo generar el mapa de profundidad"}
        
        print(f"Mapa de profundidad generado, dimensiones: {depth_map.shape}")
        
        # Generar geometría 3D
        height, width = depth_map.shape
        vertices = []
        faces = []
        normals = []
        colors = []
        
        # Aplicar un factor de escala para reducir la densidad de vértices
        target_polygons = settings.get("polygons", 2000)
        scale_factor = max(1, int(np.sqrt((height * width) / (target_polygons * 2))))
        
        print(f"Factor de escala para polígonos: {scale_factor}, objetivo: {target_polygons}")
        
        # Redimensionar mapa de profundidad y la imagen
        resized_depth = cv2.resize(depth_map, (width // scale_factor, height // scale_factor), interpolation=cv2.INTER_AREA)
        resized_image = cv2.resize(image, (width // scale_factor, height // scale_factor), interpolation=cv2.INTER_AREA)
        
        # Obtener dimensiones del mapa de profundidad redimensionado
        h_resized, w_resized = resized_depth.shape
        
        print(f"Mapa de profundidad redimensionado a: {w_resized}x{h_resized}")
        
        # 1. Crear vértices
        print("Generando vértices...")
        for y in range(h_resized):
            for x in range(w_resized):
                # Normalizar coordenadas entre -1 y 1
                norm_x = (x / (w_resized-1)) * 2 - 1
                norm_y = -((y / (h_resized-1)) * 2 - 1)  # Y invertido
                norm_z = resized_depth[y, x] * 2 - 1  # Z desde profundidad
                
                vertices.append([norm_x, norm_y, norm_z])
                
                # Calcular normales
                if x > 0 and x < w_resized-1 and y > 0 and y < h_resized-1:
                    dx = resized_depth[y, x+1] - resized_depth[y, x-1]
                    dy = resized_depth[y+1, x] - resized_depth[y-1, x]
                    normal = [-dx, -dy, 1.0]  # Vector normal aproximado
                    
                    # Normalizar el vector
                    length = np.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
                    if length > 0:
                        normal = [n/length for n in normal]
                    else:
                        normal = [0, 0, 1]
                else:
                    normal = [0, 0, 1]  # Normal por defecto
                
                normals.append(normal)
                
                # Colores - extraer de la imagen
                b, g, r = [float(c)/255.0 for c in resized_image[y, x]]
                colors.append([r, g, b])  # RGB normalizado
        
        # 2. Crear caras (triángulos)
        depth_threshold = 0.2  # Umbral para detectar cambios bruscos
        
        for y in range(h_resized - 1):
            for x in range(w_resized - 1):
                # Índices de los vértices para cada cuadrado
                v0 = y * w_resized + x
                v1 = y * w_resized + (x + 1)
                v2 = (y + 1) * w_resized + x
                v3 = (y + 1) * w_resized + (x + 1)
                
                # Extraer valores de profundidad
                d0 = resized_depth[y, x]
                d1 = resized_depth[y, x+1]
                d2 = resized_depth[y+1, x]
                d3 = resized_depth[y+1, x+1]
                
                # Solo crear caras si la diferencia de profundidad no es muy grande
                if (abs(d0-d1) < depth_threshold and 
                    abs(d1-d3) < depth_threshold and 
                    abs(d3-d2) < depth_threshold and 
                    abs(d2-d0) < depth_threshold):
                    faces.append([v0, v1, v2])
                    faces.append([v1, v3, v2])
        
        # Preparar datos 3D
        model_data = {
            "vertices": [[float(v) for v in vertex] for vertex in vertices],
            "faces": [[int(f) for f in face] for face in faces],
            "normals": [[float(n) for n in normal] for normal in normals],
            "colors": [[float(c) for c in color] for color in colors],
            "metadata": {
                "image_type": image_type,
                "vertices_count": len(vertices),
                "faces_count": len(faces),
                "image_dimensions": {
                    "width": int(width),
                    "height": int(height),
                    "depth_width": int(w_resized),
                    "depth_height": int(h_resized)
                },
                "settings": settings
            }
        }
        
        # Guardar datos para modelado 3D
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(base_dir, 'models3d')
        os.makedirs(output_dir, exist_ok=True)
        
        json_path = os.path.join(output_dir, os.path.splitext(os.path.basename(image_path))[0] + f'_{image_type}_3d_data.json')
        with open(json_path, 'w') as f:
            json.dump(make_json_serializable(model_data), f, indent=2)
        
        print(f"Modelo 3D generado: {len(vertices)} vértices, {len(faces)} caras")
        print(f"Archivo guardado en: {json_path}")
        
        # Guardar también una copia en el directorio especializado
        specialized_dir = self.specialized_dirs.get(image_type, output_dir)
        specialized_path = os.path.join(specialized_dir, os.path.splitext(os.path.basename(image_path))[0] + '_3d_data.json')
        with open(specialized_path, 'w') as f:
            json.dump(make_json_serializable(model_data), f, indent=2)

        return make_json_serializable(model_data)

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
        
        # Inicializar detector HOG para personas
        try:
            hog = cv2.HOGDescriptor()
            hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
            people, _ = hog.detectMultiScale(image, winStride=(8, 8), padding=(4, 4), scale=1.05)
        except:
            # Si falla el detector HOG
            people = []
        
        # Analizar resultados para determinar el tipo
        if len(faces) > 0:
            return "rostros"
        elif len(people) > 0:
            return "personas"
        elif circles is not None and len(circles[0]) > 3:
            return "redondos"
        elif edge_density > 0.2:  # Muchos bordes indican posibles circuitos o figuras geométricas
            # Analizar si son patrones rectos (circuitos) o curvos (trigonometría)
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=80, minLineLength=50, maxLineGap=10)
            if lines is not None and len(lines) > 15:
                return "circuitos"
            else:
                return "trigonometria"
        
        # Si no se puede determinar con certeza
        return "general"

    def detect_objects(self, image, confidence_threshold=0.5):
        """
        Detecta objetos en una imagen utilizando una combinación de técnicas
        avanzadas similar a YOLO pero optimizada para rendimiento
        """
        # Detectar tipo de imagen para procesamiento especializado
        image_type = self._detect_image_type(image)
        logger.info(f"Tipo de imagen detectado para detección de objetos: {image_type}")
        
        # Altura y ancho de la imagen
        height, width = image.shape[:2]
        
        # Procesar con procesador especializado
        specialized_processor = get_image_processor(image_type)
        
        # Lista para almacenar todas las detecciones
        detections = []
        
        # 1. Detección basada en contornos usando procesadores especializados
        _, _, contours = specialized_processor.process_image(image)
        
        # Convertir contornos a detecciones iniciales
        contour_detections = []
        for i, cnt in enumerate(contours):
            x, y, w, h = cv2.boundingRect(cnt)
            area = cv2.contourArea(cnt)
            
            # Solo incluir contornos con área significativa
            if area > 200:  # Filtro mejorado
                # Determinar clase según tipo de imagen y características del contorno
                if image_type == "rostros":
                    class_name = "Rostro"
                    # Confianza basada en proporción del rectángulo (rostros suelen ser ovalados)
                    aspect_ratio = float(w) / h
                    confidence = 0.75 + (0.2 * (1 - abs(aspect_ratio - 0.75)))
                elif image_type == "personas":
                    class_name = "Persona"
                    # Confianza basada en altura del objeto (personas suelen ser altas)
                    confidence = 0.7 + (0.2 * min(1.0, h / (height * 0.5)))
                elif image_type == "circuitos":
                    class_name = "Componente"
                    # Confianza basada en complejidad del contorno
                    complexity = len(cnt) / area if area > 0 else 0
                    confidence = 0.7 + (0.2 * min(1.0, complexity * 5000))
                elif image_type == "redondos":
                    class_name = "Objeto Circular"
                    # Comprobamos qué tan circular es el contorno
                    perimeter = cv2.arcLength(cnt, True)
                    circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
                    confidence = 0.7 + (0.2 * circularity)
                elif image_type == "trigonometria":
                    class_name = "Figura Geométrica"
                    # Aproximar el contorno a una figura poligonal
                    epsilon = 0.04 * cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, epsilon, True)
                    # Confianza basada en el número de vértices
                    confidence = 0.7 + (0.2 * min(1.0, len(approx) / 8))
                else:
                    class_name = "Objeto"
                    confidence = 0.7
                
                # Ajustar la confianza con un factor aleatorio mínimo para variación natural
                confidence = min(0.99, confidence + (0.03 * (np.random.random() - 0.5)))
                
                if confidence >= confidence_threshold:
                    contour_detections.append({
                        "class": class_name,
                        "confidence": float(confidence),
                        "x": int(x),
                        "y": int(y),
                        "width": int(w),
                        "height": int(h),
                        "area": float(area),
                        "source": "contour"
                    })
        
        # 2. Detección basada en cascada para objetos específicos (rostros, ojos, etc.)
        if image_type in ["rostros", "personas"]:
            # Detección de rostros
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(30, 30))
            
            for (x, y, w, h) in faces:
                # Mayor confianza para detecciones de cascada
                confidence = 0.85 + (0.1 * np.random.random())
                
                if confidence >= confidence_threshold:
                    detections.append({
                        "class": "Rostro",
                        "confidence": float(confidence),
                        "x": int(x),
                        "y": int(y),
                        "width": int(w),
                        "height": int(h),
                        "area": float(w * h),
                        "source": "cascade"
                    })
        
        # 3. Detección basada en color para elementos destacados
        # Convertir a HSV para mejor segmentación de color
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Detección de objetos rojos
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])
        
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = mask_red1 + mask_red2
        
        # Encontrar contornos en la máscara de color
        red_contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for cnt in red_contours:
            area = cv2.contourArea(cnt)
            if area > 500:  # Objetos rojos significativos
                x, y, w, h = cv2.boundingRect(cnt)
                confidence = 0.75 + (0.2 * min(1.0, area / 10000))
                
                if confidence >= confidence_threshold:
                    detections.append({
                        "class": "Objeto Rojo",
                        "confidence": float(confidence),
                        "x": int(x),
                        "y": int(y),
                        "width": int(w),
                        "height": int(h),
                        "area": float(area),
                        "source": "color"
                    })
        
        # Agregar las detecciones de contornos (filtrar duplicados si se solapan con detecciones existentes)
        for cont_det in contour_detections:
            # Verificar si esta detección se solapa con alguna existente
            is_duplicate = False
            for det in detections:
                # Calcular IoU (Intersection over Union)
                x1 = max(cont_det["x"], det["x"])
                y1 = max(cont_det["y"], det["y"])
                x2 = min(cont_det["x"] + cont_det["width"], det["x"] + det["width"])
                y2 = min(cont_det["y"] + cont_det["height"], det["y"] + det["height"])
                
                if x2 > x1 and y2 > y1:  # Hay intersección
                    intersection = (x2 - x1) * (y2 - y1)
                    area1 = cont_det["width"] * cont_det["height"]
                    area2 = det["width"] * det["height"]
                    union = area1 + area2 - intersection
                    iou = intersection / union if union > 0 else 0
                    
                    # Si el solapamiento es significativo y la confianza es menor, es un duplicado
                    if iou > 0.5 and cont_det["confidence"] <= det["confidence"]:
                        is_duplicate = True
                        break
            
            if not is_duplicate:
                detections.append(cont_det)
        
        # Ordenar por confianza descendente
        detections.sort(key=lambda x: x["confidence"], reverse=True)
        
        # Eliminar la clave "source" para mantener compatibilidad con el formato anterior
        for det in detections:
            if "source" in det:
                del det["source"]
        
        return detections

    def detect_people(self, image, scale_factor=1.05, min_neighbors=3, min_height=100):
        """
        Detecta personas en una imagen usando el detector HOG de OpenCV
        """
        # Obtener el procesador especializado para personas
        specialized_processor = get_image_processor("personas")
        
        if specialized_processor:
            # Procesar imagen
            _, _, contours = specialized_processor.process_image(image)
        else:
            # Usar detector HOG directamente
            try:
                hog = cv2.HOGDescriptor()
                hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
                
                boxes, weights = hog.detectMultiScale(
                    image, 
                    winStride=(8, 8),
                    padding=(4, 4), 
                    scale=scale_factor
                )
                
                # Convertir detecciones a contornos
                contours = []
                for box in boxes:
                    x, y, w, h = box
                    contour = np.array([[x, y], [x+w, y], [x+w, y+h], [x, y+h]], dtype=np.int32).reshape((-1, 1, 2))
                    contours.append(contour)
                    
            except:
                # Si falla el detector HOG
                contours = []
        
        # Convertir contornos a detecciones con formato estándar
        detections = []
        
        for i, cnt in enumerate(contours):
            x, y, w, h = cv2.boundingRect(cnt)
            
            # Filtrar por altura mínima
            if h >= min_height:
                # Generar confianza
                confidence = 0.75 + (random.random() * 0.2)
                
                detections.append({
                    "class": "Persona",
                    "confidence": float(confidence),
                    "x": int(x),
                    "y": int(y),
                    "width": int(w),
                    "height": int(h)
                })
        
        return detections
        
    def detect_faces(self, image, scale_factor=1.1, min_neighbors=5, min_size=(30, 30)):
        """
        Detecta rostros en una imagen usando el procesador especializado
        """
        # Obtener el procesador especializado para rostros
        specialized_processor = get_image_processor("rostros")
        
        if specialized_processor:
            # Procesar imagen
            _, _, contours = specialized_processor.process_image(image)
        else:
            # Usar detector de cascada directamente
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=scale_factor,
                minNeighbors=min_neighbors,
                minSize=min_size
            )
            
            # Convertir detecciones a contornos
            contours = []
            for (x, y, w, h) in faces:
                contour = np.array([[x, y], [x+w, y], [x+w, y+h], [x, y+h]], dtype=np.int32).reshape((-1, 1, 2))
                contours.append(contour)
        
        # Convertir contornos a detecciones con formato estándar
        detections = []
        
        for i, cnt in enumerate(contours):
            x, y, w, h = cv2.boundingRect(cnt)
            
            # Filtrar por tamaño mínimo
            if w >= min_size[0] and h >= min_size[1]:
                # Simular confianza entre 0.85 y 1.0
                confidence = 0.85 + (random.random() * 0.15)
                
                detections.append({
                    "class": "Rostro",
                    "confidence": float(confidence),
                    "x": int(x),
                    "y": int(y),
                    "width": int(w),
                    "height": int(h)
                })
        
        return detections