# cython: language_level=3
import cv2
import numpy as np
cimport numpy as np
from libc.stdlib cimport malloc, free
import os

def extract_image_metadata(str image_path):
    """Extrae metadatos básicos de la imagen."""
    cdef dict metadata = {}
    img = cv2.imread(image_path)
    
    if img is not None:
        metadata['height'] = img.shape[0]
        metadata['width'] = img.shape[1]
        metadata['channels'] = img.shape[2]
        metadata['size_kb'] = img.nbytes / 1024
        
    return metadata

def process_image_yolo(str image_path, str weights_path, str config_path, float confidence_threshold=0.5):
    """Procesa la imagen usando YOLO para detección de objetos."""
    cdef dict results = {'detections': []}
    
    # Cargar imagen
    img = cv2.imread(image_path)
    if img is None:
        return results
    
    # Cargar YOLO
    net = cv2.dnn.readNet(weights_path, config_path)
    
    # Procesar imagen
    blob = cv2.dnn.blobFromImage(img, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    
    # Obtener detecciones
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    outs = net.forward(output_layers)
    
    # Procesar resultados
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            
            if confidence > confidence_threshold:
                center_x = int(detection[0] * img.shape[1])
                center_y = int(detection[1] * img.shape[0])
                w = int(detection[2] * img.shape[1])
                h = int(detection[3] * img.shape[0])
                
                results['detections'].append({
                    'class_id': int(class_id),
                    'confidence': float(confidence),
                    'bbox': [center_x, center_y, w, h]
                })
    
    return results

def optimize_image(str image_path, str output_path, int target_size_kb=500):
    """Optimiza el tamaño de la imagen manteniendo la calidad."""
    img = cv2.imread(image_path)
    if img is None:
        return False
        
    quality = 95
    while quality > 5:
        cv2.imwrite(output_path, img, [cv2.IMWRITE_JPEG_QUALITY, quality])
        size_kb = os.path.getsize(output_path) / 1024
        if size_kb <= target_size_kb:
            break
        quality -= 5
        
    return True 