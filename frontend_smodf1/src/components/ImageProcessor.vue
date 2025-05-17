<template>
  <div class="image-processor">
    <div class="processor-header">
      <h3>Procesamiento de Imagen</h3>
      <div class="processor-tabs">
        <button 
          @click="activeTab = 'detection'" 
          :class="{'active': activeTab === 'detection'}"
        >
          <i class="fas fa-search"></i> Detección
        </button>
        <button 
          @click="activeTab = 'analysis'" 
          :class="{'active': activeTab === 'analysis'}"
        >
          <i class="fas fa-chart-pie"></i> Análisis
        </button>
        <button 
          @click="activeTab = 'metadata'" 
          :class="{'active': activeTab === 'metadata'}"
        >
          <i class="fas fa-info-circle"></i> Metadatos
        </button>
        <button 
          @click="activeTab = '3d'" 
          :class="{'active': activeTab === '3d'}"
          :disabled="!image.processed"
        >
          <i class="fas fa-cube"></i> Modelo 3D
        </button>
      </div>
    </div>

    <div class="processor-content">
      <!-- Pestaña de Detección -->
      <div v-if="activeTab === 'detection'" class="tab-content detection-tab">
        <div class="image-preview">
          <img 
            :src="image.processed_image || image.image" 
            alt="Imagen procesada" 
            ref="detectionCanvas"
            @load="drawDetectionOverlay"
          />
          <canvas v-if="image.processed" class="detection-overlay" ref="overlayCanvas"></canvas>
        </div>
        <div class="detection-controls">
          <div class="control-group">
            <label>Sensibilidad de detección</label>
            <input type="range" v-model="detectionSettings.sensitivity" min="0" max="1" step="0.1">
            <span>{{ detectionSettings.sensitivity }}</span>
          </div>
          <div class="control-group">
            <label>Tipos de objetos</label>
            <div class="object-types">
              <label v-for="(type, index) in detectionSettings.objectTypes" :key="index">
                <input type="checkbox" v-model="type.active">
                {{ type.name }}
              </label>
            </div>
          </div>
          <button @click="reprocessImage" class="btn-process-again">
            <i class="fas fa-redo"></i> Procesar de nuevo
          </button>
        </div>
        <div class="detection-results" v-if="image.processed && image.analysis_results">
          <h4>Objetos Detectados</h4>
          <div class="objects-list">
            <div 
              v-for="(obj, index) in image.analysis_results.analysis.objects" 
              :key="index"
              class="object-item"
              @mouseover="highlightObject(index)"
              @mouseout="clearHighlights"
            >
              <div class="object-info">
                <span class="object-label">{{ obj.label || 'Objeto ' + (index + 1) }}</span>
                <span class="object-confidence">{{ (obj.confidence * 100).toFixed(1) }}% confianza</span>
              </div>
              <div class="object-details">
                <span>Tamaño: {{ Math.round(obj.area) }}px²</span>
                <span>Posición: ({{ Math.round(obj.x) }}, {{ Math.round(obj.y) }})</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pestaña de Análisis -->
      <div v-if="activeTab === 'analysis'" class="tab-content analysis-tab">
        <div class="analysis-grid">
          <div class="analysis-card">
            <i class="fas fa-users"></i>
            <span class="analysis-value">{{ image.analysis_results?.analysis.faces_detected || 0 }}</span>
            <span class="analysis-label">Rostros Detectados</span>
          </div>
          <div class="analysis-card">
            <i class="fas fa-shapes"></i>
            <span class="analysis-value">{{ image.analysis_results?.analysis.objects_detected || 0 }}</span>
            <span class="analysis-label">Objetos Detectados</span>
          </div>
          <div class="analysis-card">
            <i class="fas fa-palette"></i>
            <div class="color-preview" :style="averageColorStyle"></div>
            <span class="analysis-label">Color Promedio</span>
          </div>
          <div class="analysis-card">
            <i class="fas fa-eye"></i>
            <span class="analysis-value">{{ image.analysis_results?.analysis.complexity || 'N/A' }}</span>
            <span class="analysis-label">Complejidad Visual</span>
          </div>
        </div>
        <div class="image-comparison">
          <h4>Comparación</h4>
          <div class="comparison-container">
            <div class="original-image">
              <h5>Original</h5>
              <img :src="image.image" alt="Original">
            </div>
            <div class="processed-image">
              <h5>Procesada</h5>
              <img :src="image.processed_image" alt="Procesada" v-if="image.processed_image">
              <div class="not-processed" v-else>Imagen no procesada</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pestaña de Metadatos -->
      <div v-if="activeTab === 'metadata'" class="tab-content metadata-tab">
        <div class="metadata-section">
          <h4>Información Técnica</h4>
          <div class="metadata-grid">
            <div class="metadata-item">
              <span class="metadata-label">Dimensiones</span>
              <span class="metadata-value">{{ image.image_width || 'N/A' }} x {{ image.image_height || 'N/A' }} px</span>
            </div>
            <div class="metadata-item">
              <span class="metadata-label">Tamaño de archivo</span>
              <span class="metadata-value">{{ formatSize(image.file_size) }}</span>
            </div>
            <div class="metadata-item">
              <span class="metadata-label">Fecha de captura</span>
              <span class="metadata-value">{{ image.analysis_results?.metadata?.capture_date || 'N/A' }}</span>
            </div>
            <div class="metadata-item">
              <span class="metadata-label">Cámara / Dispositivo</span>
              <span class="metadata-value">{{ image.analysis_results?.metadata?.device || 'N/A' }}</span>
            </div>
            <div class="metadata-item">
              <span class="metadata-label">Formato</span>
              <span class="metadata-value">{{ image.analysis_results?.metadata?.format || 'N/A' }}</span>
            </div>
            <div class="metadata-item">
              <span class="metadata-label">Fecha de procesamiento</span>
              <span class="metadata-value">{{ formatDate(image.processing_completed) }}</span>
            </div>
          </div>
        </div>
        <div class="datasheet-section">
          <h4>Ficha Técnica</h4>
          <div class="datasheet-actions">
            <button @click="generateDatasheet" class="btn-datasheet">
              <i class="fas fa-file-pdf"></i> Generar PDF
            </button>
            <button @click="exportMetadata" class="btn-export">
              <i class="fas fa-file-export"></i> Exportar JSON
            </button>
          </div>
          <div class="datasheet-preview">
            <pre>{{ formatDatasheet() }}</pre>
          </div>
        </div>
      </div>

      <!-- Pestaña de Modelo 3D -->
      <div v-if="activeTab === '3d'" class="tab-content model-3d-tab">
        <div v-if="image.has_3d_data" class="model-3d-container">
          <div class="model-3d-viewer" ref="modelViewer">
            <!-- El canvas para Three.js se renderizará aquí -->
          </div>
          <div class="model-3d-controls">
            <button @click="rotate3DModel('left')" class="btn-rotate">
              <i class="fas fa-undo"></i>
            </button>
            <button @click="rotate3DModel('right')" class="btn-rotate">
              <i class="fas fa-redo"></i>
            </button>
            <button @click="resetView3D" class="btn-reset">
              <i class="fas fa-home"></i>
            </button>
          </div>
          <div class="model-3d-info">
            <h4>Información del Modelo</h4>
            <div class="model-info-grid">
              <div class="model-info-item">
                <span class="info-label">Puntos clave</span>
                <span class="info-value">{{ image.data_3d?.keypoints_count || 'N/A' }}</span>
              </div>
              <div class="model-info-item">
                <span class="info-label">Dimensiones</span>
                <span class="info-value">{{ image.data_3d?.image_dimensions?.width || 'N/A' }} x {{ image.data_3d?.image_dimensions?.height || 'N/A' }}</span>
              </div>
              <div class="model-info-item">
                <span class="info-label">Escala</span>
                <span class="info-value">{{ image.data_3d?.scale || 'N/A' }}</span>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="no-3d-data">
          <i class="fas fa-cube"></i>
          <p>No hay datos 3D disponibles para esta imagen</p>
          <button @click="generate3D" class="btn-generate-3d">
            <i class="fas fa-magic"></i> Generar Modelo 3D
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from '@/utils/axios';

export default {
  name: 'ImageProcessor',
  props: {
    image: {
      type: Object,
      required: true
    },
    projectId: {
      type: [Number, String],
      required: true
    }
  },
  data() {
    return {
      activeTab: 'detection',
      detectionSettings: {
        sensitivity: 0.5,
        objectTypes: [
          { name: 'Personas', active: true },
          { name: 'Vehículos', active: true },
          { name: 'Edificios', active: true },
          { name: 'Mobiliario', active: true },
          { name: 'Objetos', active: true }
        ]
      },
      loading: false,
      loadingMessage: ''
    }
  },
  computed: {
    averageColorStyle() {
      if (this.image.analysis_results?.analysis.average_color) {
        const color = this.image.analysis_results.analysis.average_color;
        return {
          backgroundColor: `rgb(${color.r}, ${color.g}, ${color.b})`
        };
      }
      return { backgroundColor: '#cccccc' };
    }
  },
  mounted() {
    if (this.image.processed && this.activeTab === 'detection') {
      this.$nextTick(() => {
        this.drawDetectionOverlay();
      });
    }
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return 'N/A';
      return new Date(dateString).toLocaleString();
    },
    formatSize(bytes) {
      if (!bytes) return 'N/A';
      const kb = bytes / 1024;
      return kb > 1024 ? `${(kb/1024).toFixed(2)} MB` : `${kb.toFixed(2)} KB`;
    },
    drawDetectionOverlay() {
      if (!this.image.processed || !this.image.analysis_results) return;
      
      const img = this.$refs.detectionCanvas;
      const canvas = this.$refs.overlayCanvas;
      
      if (!img || !canvas) return;
      
      canvas.width = img.width;
      canvas.height = img.height;
      
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      const objects = this.image.analysis_results.analysis.objects || [];
      objects.forEach(obj => {
        ctx.strokeStyle = 'rgba(255, 0, 0, 0.7)';
        ctx.lineWidth = 2;
        ctx.strokeRect(obj.x - obj.width/2, obj.y - obj.height/2, obj.width, obj.height);
        
        ctx.fillStyle = 'rgba(255, 0, 0, 0.7)';
        ctx.font = '12px Arial';
        ctx.fillText(obj.label || 'Objeto', obj.x - obj.width/2, obj.y - obj.height/2 - 5);
      });
    },
    highlightObject(index) {
      const canvas = this.$refs.overlayCanvas;
      if (!canvas) return;
      
      const ctx = canvas.getContext('2d');
      this.drawDetectionOverlay(); // Redibuja todo
      
      const obj = this.image.analysis_results.analysis.objects[index];
      if (obj) {
        // Destaca el objeto seleccionado
        ctx.strokeStyle = 'rgba(0, 255, 0, 0.9)';
        ctx.lineWidth = 3;
        ctx.strokeRect(obj.x - obj.width/2, obj.y - obj.height/2, obj.width, obj.height);
      }
    },
    clearHighlights() {
      this.drawDetectionOverlay(); // Vuelve a dibujar todo normalmente
    },
    async reprocessImage() {
      this.loading = true;
      this.loadingMessage = 'Reprocesando imagen...';
      
      try {
        const response = await axiosInstance.post(
          `/api/projects/${this.projectId}/process_image/`,
          {
            image_id: this.image.id,
            settings: this.detectionSettings
          }
        );
        
        // Emitir evento para indicar que la imagen ha sido reprocesada
        this.$emit('image-processed', response.data);
      } catch (error) {
        console.error('Error al reprocesar la imagen:', error);
        alert('Error al reprocesar la imagen. Por favor, inténtalo de nuevo.');
      } finally {
        this.loading = false;
      }
    },
    async generate3D() {
      this.loading = true;
      this.loadingMessage = 'Generando modelo 3D...';
      
      try {
        const response = await axiosInstance.post(
          `/api/projects/${this.projectId}/generate_3d/`,
          {
            image_id: this.image.id
          }
        );
        
        // Emitir evento para indicar que se ha generado el modelo 3D
        this.$emit('model-generated', response.data);
        
        // Cambiar a la pestaña 3D
        this.activeTab = '3d';
      } catch (error) {
        console.error('Error al generar el modelo 3D:', error);
        alert('Error al generar el modelo 3D. Por favor, inténtalo de nuevo.');
      } finally {
        this.loading = false;
      }
    },
    rotate3DModel(direction) {
      // Esta función sería implementada con Three.js para rotar el modelo 3D
      console.log(`Rotando modelo en dirección: ${direction}`);
    },
    resetView3D() {
      // Resetear la vista del modelo 3D
      console.log('Vista del modelo 3D reseteada');
    },
    generateDatasheet() {
      // Implementar la generación de PDF con una biblioteca como jsPDF
      alert('Generación de PDF implementada en la siguiente fase');
    },
    exportMetadata() {
      // Generar un archivo JSON con los metadatos
      const metadataStr = JSON.stringify(this.image.analysis_results || {}, null, 2);
      const blob = new Blob([metadataStr], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      
      // Crear enlace para descargar
      const a = document.createElement('a');
      a.href = url;
      a.download = `metadata_image_${this.image.id}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    },
    formatDatasheet() {
      if (!this.image.analysis_results) return 'No hay datos disponibles';
      
      const analysis = this.image.analysis_results.analysis || {};
      const metadata = this.image.analysis_results.metadata || {};
      
      return JSON.stringify({
        filename: this.image.image.split('/').pop(),
        dimensions: `${this.image.image_width || 'N/A'} x ${this.image.image_height || 'N/A'} px`,
        fileSize: this.formatSize(this.image.file_size),
        format: metadata.format || 'N/A',
        captureDevice: metadata.device || 'N/A',
        captureDate: metadata.capture_date || 'N/A',
        processingDate: this.formatDate(this.image.processing_completed),
        analysisResults: {
          objectsDetected: analysis.objects_detected || 0,
          facesDetected: analysis.faces_detected || 0,
          complexity: analysis.complexity || 'N/A',
          averageColor: analysis.average_color || { r: 0, g: 0, b: 0 }
        }
      }, null, 2);
    }
  },
  watch: {
    activeTab(newTab) {
      if (newTab === 'detection' && this.image.processed) {
        this.$nextTick(() => {
          this.drawDetectionOverlay();
        });
      }
    }
  }
}
</script>

<style scoped>
.image-processor {
  background-color: #f5f5f5;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin-bottom: 2rem;
}

.processor-header {
  background-color: #2c3e50;
  color: white;
  padding: 1rem;
}

.processor-header h3 {
  margin: 0 0 1rem 0;
}

.processor-tabs {
  display: flex;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.processor-tabs button {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s;
}

.processor-tabs button:hover {
  color: white;
}

.processor-tabs button.active {
  color: white;
  border-bottom: 3px solid #3498db;
}

.processor-tabs button:disabled {
  color: rgba(255, 255, 255, 0.3);
  cursor: not-allowed;
}

.processor-content {
  padding: 1.5rem;
}

.tab-content {
  min-height: 300px;
}

/* Estilos para la pestaña de detección */
.detection-tab {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.image-preview {
  flex: 1;
  min-width: 300px;
  position: relative;
}

.image-preview img {
  max-width: 100%;
  border-radius: 4px;
}

.detection-overlay {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: none;
}

.detection-controls {
  width: 250px;
}

.control-group {
  margin-bottom: 1rem;
}

.control-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

.object-types label {
  display: block;
  margin-bottom: 0.3rem;
  font-weight: normal;
}

.btn-process-again {
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  width: 100%;
  margin-top: 1rem;
}

.detection-results {
  width: 100%;
  margin-top: 1rem;
}

.objects-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 0.5rem;
}

.object-item {
  background-color: white;
  border-radius: 4px;
  padding: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.2s;
}

.object-item:hover {
  background-color: #f0f7ff;
}

.object-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.3rem;
}

.object-label {
  font-weight: bold;
}

.object-confidence {
  color: #2ecc71;
}

.object-details {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #7f8c8d;
}

/* Estilos para la pestaña de análisis */
.analysis-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.analysis-card {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.analysis-card i {
  font-size: 2rem;
  color: #3498db;
  margin-bottom: 0.5rem;
}

.analysis-value {
  display: block;
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.analysis-label {
  display: block;
  font-size: 0.9rem;
  color: #7f8c8d;
}

.color-preview {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin: 0.5rem auto;
  border: 2px solid #e0e0e0;
}

.image-comparison {
  margin-top: 1.5rem;
}

.comparison-container {
  display: flex;
  gap: 1rem;
}

.original-image, .processed-image {
  flex: 1;
}

.original-image h5, .processed-image h5 {
  text-align: center;
  margin-bottom: 0.5rem;
}

.original-image img, .processed-image img {
  max-width: 100%;
  border-radius: 4px;
}

.not-processed {
  height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f0f0f0;
  border-radius: 4px;
  color: #7f8c8d;
}

/* Estilos para la pestaña de metadatos */
.metadata-tab {
  display: flex;
  gap: 2rem;
}

.metadata-section, .datasheet-section {
  flex: 1;
}

.metadata-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem 1.5rem;
}

.metadata-item {
  margin-bottom: 0.5rem;
}

.metadata-label {
  display: block;
  font-size: 0.8rem;
  color: #7f8c8d;
}

.metadata-value {
  font-weight: bold;
}

.datasheet-actions {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.btn-datasheet, .btn-export {
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  flex: 1;
}

.btn-export {
  background-color: #2ecc71;
}

.datasheet-preview {
  background-color: white;
  border-radius: 4px;
  padding: 1rem;
  font-family: monospace;
  font-size: 0.8rem;
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #e0e0e0;
}

/* Estilos para la pestaña de modelo 3D */
.model-3d-container {
  display: flex;
  flex-direction: column;
  height: 500px;
}

.model-3d-viewer {
  flex: 1;
  background-color: #1a1a1a;
  border-radius: 4px;
  position: relative;
}

.model-3d-controls {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin: 1rem 0;
}

.btn-rotate, .btn-reset {
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
}

.btn-reset {
  background-color: #7f8c8d;
}

.model-info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.model-info-item {
  background-color: white;
  border-radius: 4px;
  padding: 0.8rem;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.info-label {
  display: block;
  font-size: 0.8rem;
  color: #7f8c8d;
  margin-bottom: 0.3rem;
}

.info-value {
  font-weight: bold;
}

.no-3d-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 0;
}

.no-3d-data i {
  font-size: 3rem;
  color: #7f8c8d;
  margin-bottom: 1rem;
}

.btn-generate-3d {
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.8rem 1.5rem;
  cursor: pointer;
  margin-top: 1.5rem;
}
</style> 