import cv2
import numpy as np
import os
import logging
from abc import ABC, abstractmethod

# Configurar logging
logger = logging.getLogger(__name__)

class BaseImageProcessor(ABC):
    """Clase base para procesadores de imágenes especializados"""
    
    def __init__(self):
        self.name = "base"
    
    @abstractmethod
    def process_image(self, image):
        """
        Procesa una imagen según la especialización
        
        Args:
            image: Imagen en formato numpy array (OpenCV)
            
        Returns:
            Tuple de (imagen procesada, mapa de profundidad, contornos)
        """
        pass
    
    @abstractmethod
    def generate_depth_map(self, image, detail_level=5, sensitivity=0.5):
        """
        Genera un mapa de profundidad a partir de una imagen
        
        Args:
            image: Imagen en formato numpy array (OpenCV)
            detail_level: Nivel de detalle (1-10)
            sensitivity: Sensibilidad (0-1)
            
        Returns:
            Mapa de profundidad normalizado (0-1)
        """
        pass
    
    def extract_contours(self, image, detail_level=5, sensitivity=0.5):
        """
        Extrae contornos de una imagen
        
        Returns:
            Lista de contornos
        """
        # Convertir a escala de grises si es necesario
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Ajustar parámetros según nivel de detalle y sensibilidad
        blur_size = max(1, 11 - detail_level)
        if blur_size % 2 == 0:
            blur_size += 1  # Debe ser impar
            
        canny_low = int(100 * sensitivity)
        canny_high = int(200 * sensitivity)
        
        # Aplicar filtros
        blurred = cv2.GaussianBlur(gray, (blur_size, blur_size), 0)
        edges = cv2.Canny(blurred, canny_low, canny_high)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filtrar contornos pequeños
        min_area = 10 * detail_level
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
        
        return filtered_contours
    
    def apply_color_effect(self, image, effect='normal'):
        """
        Aplica un efecto de color a la imagen
        
        Args:
            image: Imagen en formato numpy array (OpenCV)
            effect: Efecto a aplicar ('normal', 'grayscale', 'blueprint', 'sepia', 'negative')
            
        Returns:
            Imagen con efecto aplicado
        """
        if effect == 'grayscale':
            if len(image.shape) == 3:
                result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
            return image
            
        elif effect == 'blueprint':
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image.copy()
                
            result = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)
            result[:,:,0] = 180  # Canal B (azul)
            result[:,:,1] = 30 + gray // 4  # Canal G
            result[:,:,2] = 5 + gray // 8   # Canal R
            return result
            
        elif effect == 'sepia':
            if len(image.shape) != 3:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
                
            kernel = np.array([[0.272, 0.534, 0.131],
                              [0.349, 0.686, 0.168],
                              [0.393, 0.769, 0.189]])
            return cv2.transform(image, kernel)
            
        elif effect == 'negative':
            return 255 - image
            
        # Normal (sin efecto)
        return image.copy()


class CircuitImageProcessor(BaseImageProcessor):
    """Procesador especializado para imágenes de circuitos"""
    
    def __init__(self):
        super().__init__()
        self.name = "circuitos"
    
    def process_image(self, image):
        """
        Procesa imágenes de circuitos destacando pistas y componentes
        """
        # Convertir a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Aplicar umbral adaptativo para destacar pistas
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY, 11, 2)
        
        # Extraer contornos
        contours = self.extract_contours(image)
        
        # Crear imagen procesada con contornos destacados
        processed = image.copy()
        cv2.drawContours(processed, contours, -1, (0, 255, 0), 2)
        
        # Generar mapa de profundidad
        depth_map = self.generate_depth_map(image)
        
        return processed, depth_map, contours
    
    def generate_depth_map(self, image, detail_level=5, sensitivity=0.5):
        """
        Genera un mapa de profundidad para circuitos
        """
        # Convertir a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Aplicar umbral adaptativo
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY, 11, 2)
        
        # Detectar bordes
        edges = cv2.Canny(gray, int(50 * sensitivity), int(150 * sensitivity))
        
        # Detectar líneas usando transformada de Hough
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 
                              threshold=50, 
                              minLineLength=30, 
                              maxLineGap=10)
        
        # Crear una máscara para las líneas detectadas
        line_mask = np.zeros_like(gray, dtype=np.float32)
        
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(line_mask, (x1, y1), (x2, y2), 1.0, 2)
        
        # Detectar componentes electrónicos con HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Crear máscaras para colores comunes en componentes electrónicos
        mask_green = cv2.inRange(hsv, (35, 50, 50), (85, 255, 255))  # Verde (placas)
        mask_black = cv2.inRange(hsv, (0, 0, 0), (180, 255, 30))     # Negro (chips)
        mask_blue = cv2.inRange(hsv, (100, 50, 50), (130, 255, 255))  # Azul (capacitores)
        
        # Combinar máscaras
        component_mask = (mask_green + mask_black + mask_blue) / 255.0
        
        # Crear mapa de profundidad base desde la imagen en escala de grises
        gray_norm = gray.astype(np.float32) / 255.0
        
        # Combinar todos los factores para crear el mapa de profundidad
        depth_map = (
            gray_norm * 0.3 + 
            (1.0 - gray_norm) * 0.2 +
            line_mask * 0.3 + 
            component_mask * 0.2
        )
        
        # Normalizar
        depth_map = cv2.normalize(depth_map, None, 0, 1, cv2.NORM_MINMAX)
        
        # Suavizar manteniendo bordes
        depth_map = cv2.bilateralFilter(depth_map, 9, 75, 75)
        
        return depth_map


class FaceImageProcessor(BaseImageProcessor):
    """Procesador especializado para imágenes con rostros"""
    
    def __init__(self):
        super().__init__()
        self.name = "rostros"
        
        # Cargar clasificadores de OpenCV
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    
    def process_image(self, image):
        """
        Procesa imágenes de rostros destacándolos
        """
        # Convertir a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detectar rostros
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Crear imagen procesada
        processed = image.copy()
        
        # Dibujar un rectángulo alrededor de cada rostro
        for (x, y, w, h) in faces:
            cv2.rectangle(processed, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # Región de interés para los ojos
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = processed[y:y+h, x:x+w]
            
            # Detectar ojos dentro del rostro
            eyes = self.eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
        
        # Generar mapa de profundidad
        depth_map = self.generate_depth_map(image)
        
        # Convertir rectángulos de rostros a contornos
        contours = []
        for (x, y, w, h) in faces:
            contour = np.array([[x, y], [x+w, y], [x+w, y+h], [x, y+h]], dtype=np.int32).reshape((-1, 1, 2))
            contours.append(contour)
        
        return processed, depth_map, contours
    
    def generate_depth_map(self, image, detail_level=5, sensitivity=0.5):
        """
        Genera un mapa de profundidad para rostros
        """
        # Convertir a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Crear un mapa de profundidad base
        depth_map = gray.astype(np.float32) / 255.0
        
        # Detectar rostros
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=max(3, min(8, int(4 + sensitivity * 5))),
            minSize=(30, 30)
        )
        
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
                        boost = max(0, min(1, (np.cos(dist * np.pi/2) * 0.7 + 0.3) * detail_level / 5))
                        face_mask[i, j] = boost
        
        # Combinar con el mapa de profundidad original
        enhanced_depth = depth_map * (1.0 - face_mask * 0.8) + face_mask * 0.8
        
        # Suavizar
        enhanced_depth = cv2.GaussianBlur(enhanced_depth, (5, 5), 0)
        
        return enhanced_depth


class RoundObjectProcessor(BaseImageProcessor):
    """Procesador especializado para imágenes con objetos redondos"""
    
    def __init__(self):
        super().__init__()
        self.name = "objetos_redondos"
    
    def process_image(self, image):
        """
        Procesa imágenes destacando objetos redondos
        """
        # Convertir a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Reducir ruido
        gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2)
        
        # Detectar círculos
        circles = cv2.HoughCircles(
            gray_blurred,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=50,
            param1=100,
            param2=30,
            minRadius=10,
            maxRadius=300
        )
        
        # Crear imagen procesada
        processed = image.copy()
        
        # Lista para guardar contornos
        contours = []
        
        # Dibujar círculos detectados
        if circles is not None:
            circles = np.uint16(np.around(circles))
            
            for i in circles[0, :]:
                # Dibujar círculo exterior
                cv2.circle(processed, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # Dibujar centro
                cv2.circle(processed, (i[0], i[1]), 2, (0, 0, 255), 3)
                
                # Crear contorno para este círculo
                # Generar puntos alrededor de la circunferencia
                contour_points = []
                for angle in range(0, 360, 10):  # Incrementos de 10 grados
                    x = int(i[0] + i[2] * np.cos(np.radians(angle)))
                    y = int(i[1] + i[2] * np.sin(np.radians(angle)))
                    contour_points.append([[x, y]])
                
                contours.append(np.array(contour_points, dtype=np.int32))
        
        # Generar mapa de profundidad
        depth_map = self.generate_depth_map(image)
        
        return processed, depth_map, contours
    
    def generate_depth_map(self, image, detail_level=5, sensitivity=0.5):
        """
        Genera un mapa de profundidad para objetos redondos
        """
        # Convertir a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Reducir ruido
        gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2)
        
        # Detectar círculos con parámetros ajustados según sensibilidad
        param2 = 30 + int((1 - sensitivity) * 20)  # Más sensible con valores más bajos
        
        circles = cv2.HoughCircles(
            gray_blurred,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=50,
            param1=100,
            param2=param2,
            minRadius=10,
            maxRadius=300
        )
        
        # Crear mapa de profundidad base
        depth_map = gray.astype(np.float32) / 255.0
        
        # Crear una máscara para los círculos
        circle_mask = np.zeros_like(depth_map)
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            
            for i in circles[0, :]:
                # Dibujar círculo con gradiente radial
                center = (i[0], i[1])
                radius = i[2]
                
                # Crear máscara circular con gradiente
                for y in range(max(0, center[1]-radius), min(depth_map.shape[0], center[1]+radius+1)):
                    for x in range(max(0, center[0]-radius), min(depth_map.shape[1], center[0]+radius+1)):
                        dist = np.sqrt((x - center[0])**2 + (y - center[1])**2)
                        if dist <= radius:
                            # Crear un abultamiento para el círculo
                            # Ajustar según nivel de detalle
                            boost_factor = detail_level / 5
                            boost = (np.cos(dist/radius * np.pi/2) * 0.5 + 0.5) * boost_factor
                            circle_mask[y, x] = max(circle_mask[y, x], boost)
        
        # Combinar con el mapa de profundidad original
        enhanced_depth = depth_map * (1.0 - circle_mask * 0.7) + circle_mask * 0.7
        
        # Suavizar
        enhanced_depth = cv2.bilateralFilter(enhanced_depth, 9, 75, 75)
        
        return enhanced_depth


class TrigonometricObjectProcessor(BaseImageProcessor):
    """Procesador especializado para imágenes con objetos trigonométricos"""
    
    def __init__(self):
        super().__init__()
        self.name = "objetostrigonometria"
    
    def process_image(self, image):
        """
        Procesa imágenes destacando objetos trigonométricos
        """
        # Convertir a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detectar bordes
        edges = cv2.Canny(gray, 50, 150)
        
        # Detectar líneas
        lines = cv2.HoughLinesP(
            edges, 
            rho=1, 
            theta=np.pi/180, 
            threshold=40, 
            minLineLength=30, 
            maxLineGap=10
        )
        
        # Crear imagen procesada
        processed = image.copy()
        
        # Dibujar líneas
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(processed, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Extraer contornos
        contours = self.extract_contours(image)
        
        # Dibujar contornos
        cv2.drawContours(processed, contours, -1, (0, 0, 255), 2)
        
        # Generar mapa de profundidad
        depth_map = self.generate_depth_map(image)
        
        return processed, depth_map, contours
    
    def generate_depth_map(self, image, detail_level=5, sensitivity=0.5):
        """
        Genera un mapa de profundidad para objetos trigonométricos
        """
        # Convertir a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detectar bordes
        edges = cv2.Canny(gray, int(50 * sensitivity), int(150 * sensitivity))
        
        # Detectar líneas
        lines = cv2.HoughLinesP(
            edges, 
            rho=1, 
            theta=np.pi/180, 
            threshold=40, 
            minLineLength=30, 
            maxLineGap=10
        )
        
        # Crear mapa para líneas
        line_mask = np.zeros_like(gray, dtype=np.float32)
        
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(line_mask, (x1, y1), (x2, y2), 255, 2)
        
        # Normalizar máscara de líneas
        line_mask = line_mask / 255.0
        
        # Crear triángulos y polígonos a partir de contornos para mapeo 3D
        contours = self.extract_contours(image, detail_level, sensitivity)
        
        # Crear máscara de polígonos
        poly_mask = np.zeros_like(gray, dtype=np.float32)
        cv2.drawContours(poly_mask, contours, -1, 255, -1)
        poly_mask = poly_mask / 255.0
        
        # Crear mapa de profundidad base desde la imagen en escala de grises
        gray_norm = gray.astype(np.float32) / 255.0
        
        # Combinar los mapas con pesos que dependen del nivel de detalle
        w1 = 0.4  # Peso para escala de grises
        w2 = 0.3 * (detail_level / 5.0)  # Peso para líneas
        w3 = 0.3 * (detail_level / 5.0)  # Peso para polígonos
        
        depth_map = (gray_norm * w1 + line_mask * w2 + poly_mask * w3) / (w1 + w2 + w3)
        
        # Aplicar filtro bilateral para suavizar manteniendo bordes
        depth_map = cv2.bilateralFilter(depth_map, 9, 75, 75)
        
        return depth_map


class PersonImageProcessor(BaseImageProcessor):
    """Procesador especializado para imágenes con personas"""
    
    def __init__(self):
        super().__init__()
        self.name = "personas"
        
        # Inicializar detector HOG para personas
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    
    def process_image(self, image):
        """
        Procesa imágenes destacando personas
        """
        # Detectar personas
        boxes, weights = self.hog.detectMultiScale(
            image, 
            winStride=(8, 8),
            padding=(4, 4), 
            scale=1.05
        )
        
        # Crear imagen procesada
        processed = image.copy()
        
        # Lista para guardar contornos
        contours = []
        
        # Dibujar cuadros alrededor de las personas
        for i, (x, y, w, h) in enumerate(boxes):
            cv2.rectangle(processed, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Crear un contorno rectangular para cada persona
            contour = np.array([[x, y], [x+w, y], [x+w, y+h], [x, y+h]], dtype=np.int32).reshape((-1, 1, 2))
            contours.append(contour)
            
            # Añadir texto con confianza
            confidence = weights[i] if i < len(weights) else 0.0
            cv2.putText(processed, f"Persona: {confidence:.2f}", 
                       (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Generar mapa de profundidad
        depth_map = self.generate_depth_map(image)
        
        return processed, depth_map, contours
    
    def generate_depth_map(self, image, detail_level=5, sensitivity=0.5):
        """
        Genera un mapa de profundidad para personas
        """
        # Convertir a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Crear un mapa de profundidad base
        depth_map = gray.astype(np.float32) / 255.0
        
        # Detectar personas con parámetros ajustados según sensibilidad
        scale = 1.05 + (1 - sensitivity) * 0.1
        
        boxes, _ = self.hog.detectMultiScale(
            image, 
            winStride=(8, 8),
            padding=(4, 4), 
            scale=scale
        )
        
        # Crear una máscara para personas
        person_mask = np.zeros_like(depth_map)
        
        for (x, y, w, h) in boxes:
            # Crear gradiente vertical para cada persona (cabeza más alta que pies)
            for i in range(y, y + h):
                height_factor = 1 - (i - y) / h  # 1 en la parte superior, 0 en la parte inferior
                boost = height_factor * detail_level / 5
                
                for j in range(x, x + w):
                    person_mask[i, j] = max(person_mask[i, j], boost)
        
        # Combinar con el mapa de profundidad original
        enhanced_depth = depth_map * 0.5 + person_mask * 0.5
        
        # Suavizar
        enhanced_depth = cv2.GaussianBlur(enhanced_depth, (5, 5), 0)
        
        return enhanced_depth


class DefaultImageProcessor(BaseImageProcessor):
    """Procesador genérico para cualquier tipo de imagen"""
    
    def __init__(self):
        super().__init__()
        self.name = "default"
    
    def process_image(self, image):
        """
        Implementación por defecto de procesamiento de imagen
        """
        # Crear una copia de la imagen original
        processed = image.copy()
        
        # Extraer contornos básicos
        contours = self.extract_contours(image)
        
        # Dibujar contornos en la imagen
        cv2.drawContours(processed, contours, -1, (0, 255, 0), 2)
        
        # Generar mapa de profundidad
        depth_map = self.generate_depth_map(image)
        
        return processed, depth_map, contours
    
    def generate_depth_map(self, image, detail_level=5, sensitivity=0.5):
        """
        Implementación por defecto de generación de mapa de profundidad
        """
        # Convertir a escala de grises si la imagen es a color
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Aplicar filtro bilateral para reducir ruido manteniendo bordes
        blurred = cv2.bilateralFilter(gray, 9, 75, 75)
        
        # Detectar bordes
        edges = cv2.Canny(blurred, int(100 * sensitivity), int(200 * sensitivity))
        
        # Crear un mapa de profundidad básico a partir de la escala de grises
        depth_map = gray.astype(np.float32) / 255.0
        
        # Crear máscara de bordes
        edge_mask = edges.astype(np.float32) / 255.0
        
        # Combinar mapa de profundidad con bordes
        combined_map = depth_map * 0.7 + edge_mask * 0.3
        
        # Aplicar suavizado final
        final_map = cv2.GaussianBlur(combined_map, (5, 5), 0)
        
        return final_map


# Crear un factory para obtener el procesador adecuado según el tipo de imagen
def get_image_processor(image_type):
    """
    Devuelve el procesador adecuado según el tipo de imagen
    
    Args:
        image_type: Tipo de imagen ('rostros', 'circuitos', 'redondos', 'trigonometria', 'personas')
        
    Returns:
        Instancia del procesador especializado
    """
    processors = {
        'rostros': FaceImageProcessor(),
        'circuitos': CircuitImageProcessor(),
        'redondos': RoundObjectProcessor(),
        'trigonometria': TrigonometricObjectProcessor(),
        'personas': PersonImageProcessor()
    }
    
    # Devolver procesador específico o uno por defecto si no existe
    return processors.get(image_type, DefaultImageProcessor()) 