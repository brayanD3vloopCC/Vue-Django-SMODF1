<template>
  <div class="modelos-view">
    <h1>Modelos 3D</h1>
    
    <div class="modelos-container">
      <!-- Panel izquierdo: Cámara y selección de proyectos -->
      <div class="panel camera-panel">
        <h2>Captura de imagen</h2>
        
        <div class="camera-controls">
          <button @click="connectCamera" :disabled="cameraConnected" class="btn btn-primary">
            <i class="fas fa-camera"></i> Conectar cámara
          </button>
          <button @click="disconnectCamera" :disabled="!cameraConnected" class="btn btn-danger">
            <i class="fas fa-stop"></i> Desconectar
          </button>
        </div>
        
        <div v-if="cameraConnected" class="video-container">
          <video ref="video" autoplay></video>
          <button @click="captureImage" class="btn btn-capture">
            <i class="fas fa-camera"></i>
          </button>
        </div>
        
        <h2 class="mt-4">Proyectos</h2>
        <select v-model="selectedProjectId" @change="loadProject" class="form-select">
          <option value="">Seleccionar proyecto</option>
          <option v-for="project in projects" :key="project.id" :value="project.id">
            {{ project.name }}
          </option>
        </select>
        
        <div v-if="currentProject" class="project-info">
          <p><strong>Nombre:</strong> {{ currentProject.name }}</p>
          <p><strong>Imágenes:</strong> {{ currentProject.images?.length || 0 }}</p>
          <p><strong>Modelos 3D:</strong> {{ models.length }}</p>
        </div>
      </div>
      
      <!-- Panel central: Previsualización -->
      <div class="panel preview-panel">
        <h2>Previsualización</h2>
        
        <div class="preview-container">
          <div v-if="capturedImage" class="image-preview">
            <img :src="capturedImage" alt="Imagen capturada" />
          </div>
          <Model3DViewer 
            v-else-if="selectedModel && modelData" 
            :modelData="modelData" 
            :colorMode="modelSettings.colorMode" 
            class="model-3d-viewer"
          />
          <div v-else class="empty-preview">
            <i class="fas fa-cube"></i>
            <p>Captura una imagen o selecciona un modelo para previsualizar</p>
          </div>
        </div>
      </div>
      
      <!-- Panel derecho: Configuración y lista de modelos -->
      <div class="panel settings-panel">
        <h2>Configuración 3D</h2>
        
        <div class="settings-form">
          <div class="form-group">
            <label>Polígonos:</label>
            <div class="range-with-value">
              <input type="range" v-model.number="modelSettings.polygons" min="100" max="10000" step="100" class="form-range" />
              <span class="range-value">{{ modelSettings.polygons }}</span>
            </div>
          </div>
          
          <div class="form-group">
            <label>Modo de color:</label>
            <select v-model="modelSettings.colorMode" class="form-select">
              <option value="color">Color</option>
              <option value="grayscale">Blanco y negro</option>
              <option value="blueprint">Azul (Blueprint)</option>
            </select>
          </div>
          
          <div class="form-group">
            <label>Calidad de imagen:</label>
            <div class="range-with-value">
              <input type="range" v-model.number="modelSettings.imageQuality" min="10" max="100" step="5" class="form-range" />
              <span class="range-value">{{ modelSettings.imageQuality }}%</span>
            </div>
          </div>
          
          <div class="form-group">
            <label>Compresión JSON:</label>
            <div class="range-with-value">
              <input type="range" v-model.number="modelSettings.jsonCompression" min="0" max="9" step="1" class="form-range" />
              <span class="range-value">{{ modelSettings.jsonCompression }}</span>
            </div>
          </div>
          
          <div class="action-buttons">
            <button @click="processImage" :disabled="!canProcess" class="btn btn-primary">
              <i class="fas fa-cogs"></i> Procesar imagen
            </button>
            <button @click="saveModel" :disabled="!modelData" class="btn btn-success">
              <i class="fas fa-save"></i> Guardar modelo
            </button>
          </div>
        </div>
        
        <h2 class="mt-4">Modelos guardados</h2>
        <div v-if="models.length > 0" class="models-list">
          <div v-for="model in models" :key="model.id" 
               class="model-item" 
               :class="{ active: selectedModel && selectedModel.id === model.id }"
               @click="selectModel(model)">
            <div class="model-name">{{ model.name || `Modelo ${model.id}` }}</div>
            <div class="model-date">{{ formatDate(model.date) }}</div>
          </div>
        </div>
        <div v-else class="no-models">
          No hay modelos guardados en este proyecto
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Model3DViewer from '@/components/Model3DViewer.vue';

// Configuración de axios
const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
});

export default {
  name: 'ModelosView',
  components: {
    Model3DViewer
  },
  data() {
    return {
      // Camera state
      cameraConnected: false,
      stream: null,
      capturedImage: null,
      
      // Projects & models
      projects: [],
      selectedProjectId: '',
      currentProject: null,
      
      // 3D Models
      models: [],
      selectedModel: null,
      modelData: null,
      
      // 3D settings
      modelSettings: {
        polygons: 2000,
        colorMode: 'color',
        imageQuality: 80, 
        jsonCompression: 6
      },
      
      // Processing state
      isProcessing: false
    }
  },
  
  computed: {
    canProcess() {
      return (this.capturedImage || this.selectedModel) && 
             this.selectedProjectId && 
             !this.isProcessing;
    }
  },
  
  mounted() {
    this.loadProjects();
  },
  
  methods: {
    // Camera methods
    async connectCamera() {
      try {
        // Conectar solo con la cámara del dispositivo
        this.stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'environment' }
        });
        
        this.$refs.video.srcObject = this.stream;
        this.cameraConnected = true;
        console.log('Cámara conectada exitosamente');
      } catch (error) {
        console.error('Error conectando cámara local:', error);
        alert('No se pudo conectar la cámara. Verifica tus permisos.');
        this.cameraConnected = false;
      }
    },
    
    disconnectCamera() {
      if (this.stream) {
        this.stream.getTracks().forEach(track => track.stop());
        this.stream = null;
      }
      
      this.cameraConnected = false;
    },
    
    captureImage() {
      if (!this.cameraConnected) return;
      
      const video = this.$refs.video;
      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0);
      
      this.capturedImage = canvas.toDataURL('image/jpeg', this.modelSettings.imageQuality / 100);
      this.selectedModel = null;
      console.log('Imagen capturada desde cámara local');
    },
    
    // Project & model methods
    async loadProjects() {
      try {
        const response = await api.get('/api/projects/');
        this.projects = response.data;
      } catch (error) {
        console.error('Error loading projects:', error);
      }
    },
    
    async loadProject() {
      if (!this.selectedProjectId) {
        this.currentProject = null;
        this.models = [];
        return;
      }
      
      try {
        const response = await api.get(`/api/projects/${this.selectedProjectId}/`);
        this.currentProject = response.data;
        
        // Obtener modelos 3D del proyecto
        this.models = this.currentProject.images
          .filter(img => img.has_3d_data)
          .map(img => ({
            id: img.id,
            name: `Modelo ${img.id}`,
            data_3d: img.data_3d,
            image: img.image
          }));
      } catch (error) {
        console.error('Error loading project:', error);
      }
    },
    
    selectModel(model) {
      this.selectedModel = model;
      this.modelData = model.data_3d;
      this.capturedImage = null;
      
      // Render 3D model
      this.$nextTick(() => {
        this.renderModel();
      });
    },
    
    // Image processing
    async processImage() {
      if (!this.canProcess) return;
      
      this.isProcessing = true;
      
      try {
        let imageId;
        
        if (this.capturedImage) {
          // Subir la imagen capturada
          const blob = await fetch(this.capturedImage).then(r => r.blob());
          const formData = new FormData();
          formData.append('image', blob, 'camera_capture.jpg');
          
          const uploadResponse = await api.post(
            `/api/projects/${this.selectedProjectId}/upload_image/`,
            formData,
            {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            }
          );
          
          imageId = uploadResponse.data.id;
        } else if (this.selectedModel) {
          imageId = this.selectedModel.id;
        }
        
        // Generar modelo 3D
        const modelResponse = await api.post(
          `/api/projects/${this.selectedProjectId}/generate_3d/`,
          {
            image_id: imageId,
            settings: {
              polygons: this.modelSettings.polygons,
              color_mode: this.modelSettings.colorMode,
              image_quality: this.modelSettings.imageQuality,
              json_compression: this.modelSettings.jsonCompression
            }
          }
        );
        
        this.modelData = modelResponse.data.results;
        
        // Actualizar modelo seleccionado o crear uno nuevo
        if (this.capturedImage) {
          const newModel = {
            id: 'model' + Date.now(),
            name: 'Nuevo modelo ' + new Date().toLocaleTimeString(),
            date: new Date().toISOString(),
            data_3d: this.modelData
          };
          
          this.models.unshift(newModel);
          this.selectedModel = newModel;
          this.capturedImage = null;
        } else if (this.selectedModel) {
          this.selectedModel.data_3d = this.modelData;
        }
        
        // Renderizar modelo
        this.$nextTick(() => {
          this.renderModel();
        });
        
        // Actualizar datos del proyecto
        await this.loadProject();
      } catch (error) {
        console.error('Error processing image:', error);
        alert('Error al procesar la imagen');
      } finally {
        this.isProcessing = false;
      }
    },
    
    async saveModel() {
      if (!this.modelData || !this.selectedProjectId) return;
      
      try {
        await api.post(
          `/api/projects/${this.selectedProjectId}/update_3d_model/`,
          {
            model_data: this.modelData,
            settings: this.modelSettings,
            image_id: this.selectedModel.id
          }
        );
        
        alert('Modelo guardado exitosamente');
        await this.loadProject();
      } catch (error) {
        console.error('Error saving model:', error);
        alert('Error al guardar el modelo');
      }
    },
    
    // 3D rendering (simplified simulation)
    renderModel() {
      if (!this.modelData || !this.$refs.canvas3d) return;
      
      const canvas = this.$refs.canvas3d;
      const ctx = canvas.getContext('2d');
      
      // Clear canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Set background
      ctx.fillStyle = '#111';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Draw a triangle (mock 3D model)
      ctx.beginPath();
      
      // Choose color based on settings
      switch (this.modelSettings.colorMode) {
        case 'grayscale':
          ctx.fillStyle = '#ccc';
          break;
        case 'blueprint':
          ctx.fillStyle = '#2389da';
          break;
        default:
          ctx.fillStyle = '#f0f0f0';
          break;
      }
      
      // Triangle vertices (center of canvas)
      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      const size = Math.min(canvas.width, canvas.height) * 0.4;
      
      ctx.moveTo(centerX, centerY - size);
      ctx.lineTo(centerX + size, centerY + size);
      ctx.lineTo(centerX - size, centerY + size);
      ctx.closePath();
      ctx.fill();
      
      // Display info
      ctx.fillStyle = '#fff';
      ctx.font = '14px Arial';
      ctx.fillText(`Modelo 3D - ${this.modelSettings.polygons} polígonos`, 10, 20);
    },
    
    // Utility methods
    formatDate(dateString) {
      if (!dateString) return '';
      
      const date = new Date(dateString);
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    }
  }
}
</script>

<style scoped>
.modelos-view {
  color: #fff;
  padding: 20px;
  min-height: 100vh;
}

.modelos-view h1 {
  margin-bottom: 20px;
  color: #a3c9e2;
  text-align: center;
}

.modelos-container {
  display: grid;
  grid-template-columns: 300px 1fr 300px;
  gap: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.panel {
  background: #1a2130;
  border-radius: 10px;
  padding: 20px;
  color: #ddd;
}

h2 {
  font-size: 1.2rem;
  margin-bottom: 15px;
  color: #a3c9e2;
  border-bottom: 1px solid #2d3a4b;
  padding-bottom: 8px;
}

.btn {
  background: #2d3a4b;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 8px;
  margin-bottom: 8px;
  font-size: 14px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn:hover {
  background: #3e4d62;
}

.btn:disabled {
  background: #1e2836;
  color: #546278;
  cursor: not-allowed;
}

.btn-primary {
  background: #2389da;
}

.btn-primary:hover {
  background: #1c75bc;
}

.btn-danger {
  background: #dc3545;
}

.btn-danger:hover {
  background: #c82333;
}

.btn-success {
  background: #28a745;
}

.btn-success:hover {
  background: #218838;
}

.video-container {
  width: 100%;
  height: 200px;
  position: relative;
  background: #000;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 15px;
}

.video-container video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.btn-capture {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(255, 255, 255, 0.3);
  color: white;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  padding: 0;
  margin: 0;
}

.form-select {
  width: 100%;
  padding: 8px 10px;
  background: #2d3a4b;
  color: white;
  border: 1px solid #3e4d62;
  border-radius: 5px;
  margin-bottom: 15px;
}

.project-info {
  font-size: 14px;
  line-height: 1.5;
}

.preview-container {
  width: 100%;
  height: 400px;
  background: #111;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.image-preview, .model-preview {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-preview img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.model-preview canvas {
  width: 100%;
  height: 100%;
}

.empty-preview {
  color: #546278;
  text-align: center;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.empty-preview i {
  font-size: 40px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-size: 14px;
  color: #a3c9e2;
}

.range-with-value {
  display: flex;
  align-items: center;
  gap: 10px;
}

.form-range {
  flex: 1;
  -webkit-appearance: none;
  height: 6px;
  background: #2d3a4b;
  border-radius: 3px;
}

.form-range::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #2389da;
  cursor: pointer;
}

.range-value {
  min-width: 40px;
  font-size: 14px;
  color: #ddd;
}

.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 25px;
}

.models-list {
  max-height: 250px;
  overflow-y: auto;
}

.model-item {
  padding: 10px;
  background: #2d3a4b;
  border-radius: 6px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.model-item:hover {
  background: #3e4d62;
}

.model-item.active {
  background: #2389da;
}

.model-name {
  font-weight: bold;
  margin-bottom: 3px;
}

.model-date {
  font-size: 12px;
  color: #a3c9e2;
}

.no-models {
  text-align: center;
  color: #546278;
  padding: 20px;
}

.mt-4 {
  margin-top: 25px;
}

/* Responsive styles */
@media (max-width: 1024px) {
  .modelos-container {
    grid-template-columns: 1fr 1fr;
    grid-template-rows: auto auto;
  }
  
  .camera-panel {
    grid-column: 1;
    grid-row: 1;
  }
  
  .preview-panel {
    grid-column: 2;
    grid-row: 1;
  }
  
  .settings-panel {
    grid-column: span 2;
    grid-row: 2;
  }
}

@media (max-width: 768px) {
  .modelos-container {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto auto;
  }
  
  .camera-panel {
    grid-column: 1;
    grid-row: 1;
  }
  
  .preview-panel {
    grid-column: 1;
    grid-row: 2;
  }
  
  .settings-panel {
    grid-column: 1;
    grid-row: 3;
  }
}
</style> 