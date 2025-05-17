<template>
  <div class="project-detail">
    <div class="project-header">
      <div class="header-left">
        <button @click="goBack" class="btn-back">
          <i class="fas fa-arrow-left"></i> Volver
        </button>
      </div>
      <div class="header-content">
        <h1>{{ project ? project.name : 'Cargando...' }}</h1>
        <div class="project-meta" v-if="project">
          <span><i class="fas fa-calendar"></i> Creado: {{ formatDate(project.created_at) }}</span>
          <span><i class="fas fa-clock"></i> Última actualización: {{ formatDate(project.updated_at) }}</span>
        </div>
      </div>
      <button @click="showUploadModal = true" class="btn-upload" v-if="project">
        <i class="fas fa-upload"></i> Subir Imagen
      </button>
    </div>

    <div class="project-content" v-if="project">
      <div class="project-info">
        <h2>Descripción</h2>
        <p>{{ project.description || 'Sin descripción' }}</p>
      </div>

      <div class="project-images">
        <h2>Imágenes del Proyecto</h2>
        <div class="images-grid" v-if="project.images && project.images.length">
          <div v-for="image in project.images" :key="image.id" class="image-card">
            <div class="image-preview">
              <img :src="image.image" :alt="'Imagen ' + image.id">
              <div class="image-overlay">
                <button @click="processImage(image)" v-if="!image.processed" class="btn-process">
                  <i class="fas fa-cogs"></i> Procesar
                </button>
                <button @click="generate3D(image)" v-if="image.processed && !image.has_3d_data" class="btn-3d">
                  <i class="fas fa-cube"></i> Generar 3D
                </button>
                <button @click="viewResults(image)" v-if="image.processed" class="btn-view">
                  <i class="fas fa-eye"></i> Ver Resultados
                </button>
              </div>
            </div>
            <div class="image-info">
              <span>Subida: {{ formatDate(image.uploaded_at) }}</span>
              <span>Estado: {{ getImageStatus(image) }}</span>
            </div>
          </div>
        </div>
        <div v-else class="no-images">
          <i class="fas fa-images"></i>
          <p>No hay imágenes en este proyecto</p>
          <button @click="showUploadModal = true" class="btn-upload">
            <i class="fas fa-upload"></i> Subir Primera Imagen
          </button>
        </div>
      </div>

      <div class="project-stats" v-if="statistics">
        <h2>Estadísticas</h2>
        <div class="stats-grid">
          <div class="stat-card">
            <i class="fas fa-image"></i>
            <span class="stat-value">{{ statistics.total_images }}</span>
            <span class="stat-label">Total de Imágenes</span>
          </div>
          <div class="stat-card">
            <i class="fas fa-check-circle"></i>
            <span class="stat-value">{{ statistics.processed_images }}</span>
            <span class="stat-label">Imágenes Procesadas</span>
          </div>
          <div class="stat-card">
            <i class="fas fa-clock"></i>
            <span class="stat-value">{{ statistics.pending_images }}</span>
            <span class="stat-label">Imágenes Pendientes</span>
          </div>
        </div>
      </div>

      <!-- Modal de Resultados -->
      <div v-if="showResultsModal" class="modal-overlay" @click="showResultsModal = false">
        <div class="modal-content results-modal" @click.stop>
          <div class="modal-header">
            <h2>Procesamiento de Imagen</h2>
            <button @click="showResultsModal = false" class="btn-close">
              <i class="fas fa-times"></i>
            </button>
          </div>
          <div class="modal-body">
            <image-processor 
              v-if="selectedImage" 
              :image="selectedImage" 
              :projectId="$route.params.id"
              @image-processed="updateImageAfterProcessing"
              @model-generated="updateImageAfterModelGeneration"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Subir Imagen -->
    <div v-if="showUploadModal" class="modal-overlay" @click="showUploadModal = false">
      <div class="modal-content" @click.stop>
        <h2>Subir Nueva Imagen</h2>
        <div class="upload-area" @drop.prevent="handleDrop" @dragover.prevent>
          <input type="file" ref="fileInput" @change="handleFileSelect" accept="image/*" style="display: none">
          <div class="upload-placeholder" @click="$refs.fileInput.click()">
            <i class="fas fa-cloud-upload-alt"></i>
            <p>Arrastra una imagen aquí o haz clic para seleccionar</p>
          </div>
        </div>
        <div v-if="uploadPreview" class="upload-preview">
          <img :src="uploadPreview" alt="Preview">
          <div class="preview-info">
            <p>{{ selectedFile.name }}</p>
            <p>{{ formatSize(selectedFile.size) }}</p>
          </div>
        </div>
        <div class="modal-actions">
          <button @click="showUploadModal = false" class="btn-cancel">Cancelar</button>
          <button @click="uploadImage" :disabled="!selectedFile" class="btn-upload">
            Subir y Procesar
          </button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading-overlay">
      <div class="loading-content">
        <i class="fas fa-spinner fa-spin"></i>
        <p>{{ loadingMessage }}</p>
      </div>
    </div>

    <div v-if="error" class="error-message">
      <i class="fas fa-exclamation-circle"></i>
      <p>{{ error }}</p>
    </div>
  </div>
</template>

<script>
import axiosInstance from '@/utils/axios';
import ImageProcessor from '@/components/ImageProcessor.vue';

export default {
  name: 'ProjectDetail',
  components: {
    ImageProcessor
  },
  data() {
    return {
      project: null,
      images: [],
      imageCount: 0,
      statistics: null,
      error: null,
      showUploadModal: false,
      selectedFile: null,
      uploadPreview: null,
      loading: false,
      loadingMessage: '',
      showResultsModal: false,
      selectedImage: null,
    }
  },
  async created() {
    await this.loadProject();
  },
  methods: {
    async loadProject() {
      try {
        this.loading = true;
        this.loadingMessage = 'Cargando proyecto...';
        const projectId = this.$route.params.id;
        
        try {
          const projectResponse = await axiosInstance.get(`/api/projects/${projectId}/`);
          this.project = projectResponse.data;
          this.images = projectResponse.data.images || [];
          this.imageCount = this.images.length;
        } catch (error) {
          console.error('Error cargando proyecto:', error);
          this.error = 'Error al cargar los detalles del proyecto';
          return;
        }
        
        try {
          const statsResponse = await axiosInstance.get(`/api/projects/${projectId}/statistics/`);
          this.statistics = statsResponse.data;
        } catch (error) {
          console.error('Error cargando estadísticas:', error);
          // Si no se pueden cargar las estadísticas, crear estadísticas básicas desde los datos del proyecto
          this.statistics = {
            total_images: this.images.length,
            processed_images: this.images.filter(img => img.processed).length,
            pending_images: this.images.filter(img => !img.processed).length,
            images_with_3d: this.images.filter(img => img.has_3d_data).length
          };
        }
      } catch (error) {
        console.error('Error general:', error);
        this.error = 'Error al cargar los datos del proyecto';
      } finally {
        this.loading = false;
      }
    },
    handleFileSelect(event) {
      const file = event.target.files[0];
      this.handleFile(file);
    },
    handleDrop(event) {
      const file = event.dataTransfer.files[0];
      this.handleFile(file);
    },
    handleFile(file) {
      if (file && file.type.startsWith('image/')) {
        this.selectedFile = file;
        const reader = new FileReader();
        reader.onload = e => this.uploadPreview = e.target.result;
        reader.readAsDataURL(file);
      }
    },
    async uploadImage() {
      if (!this.selectedFile) return;

      this.loading = true;
      this.loadingMessage = 'Subiendo y procesando imagen...';
      
      const formData = new FormData();
      formData.append('image', this.selectedFile);
      formData.append('project', this.project.id);

      try {
        await axiosInstance.post(
          `/api/project-images/`,
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        );
        
        await this.loadProject();
        this.showUploadModal = false;
        this.selectedFile = null;
        this.uploadPreview = null;
        alert('Imagen subida exitosamente');
      } catch (error) {
        console.error('Error subiendo imagen:', error);
        let errorMessage = 'Error al subir la imagen. ';
        if (error.response) {
          errorMessage += error.response.data.error || JSON.stringify(error.response.data);
        }
        alert(errorMessage);
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateString) {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    formatSize(bytes) {
      if (!bytes) return '0 KB';
      const kb = bytes / 1024;
      return kb > 1024 ? `${(kb/1024).toFixed(2)} MB` : `${kb.toFixed(2)} KB`;
    },
    async processImage(image) {
      try {
        this.loading = true;
        this.loadingMessage = 'Procesando imagen...';
        
        const response = await axiosInstance.post(
          `/api/projects/${this.project.id}/process_image/`,
          { image_id: image.id }
        );
        
        // Actualizar la imagen en la lista
        const index = this.project.images.findIndex(img => img.id === image.id);
        if (index !== -1) {
          this.project.images[index] = { ...image, ...response.data.results };
        }
        
        this.loadingMessage = 'Procesamiento completado';
        setTimeout(() => {
          this.loading = false;
          this.loadProject(); // Recargar el proyecto para obtener los datos actualizados
        }, 1000);
      } catch (error) {
        console.error('Error procesando imagen:', error);
        alert('Error al procesar la imagen');
        this.loading = false;
      }
    },
    async generate3D(image) {
      try {
        this.loading = true;
        this.loadingMessage = 'Generando datos 3D...';
        
        const response = await axiosInstance.post(
          `/api/projects/${this.project.id}/generate_3d/`,
          { image_id: image.id }
        );
        
        // Actualizar la imagen en la lista
        const index = this.project.images.findIndex(img => img.id === image.id);
        if (index !== -1) {
          this.project.images[index] = { ...image, ...response.data.results };
        }
        
        this.loadingMessage = 'Generación 3D completada';
        setTimeout(() => {
          this.loading = false;
          this.loadProject(); // Recargar el proyecto para obtener los datos actualizados
        }, 1000);
      } catch (error) {
        console.error('Error generando datos 3D:', error);
        alert('Error al generar datos 3D');
        this.loading = false;
      }
    },
    viewResults(image) {
      this.selectedImage = image;
      this.showResultsModal = true;
    },
    getImageStatus(image) {
      if (image.processed && image.has_3d_data) return 'Procesada + 3D';
      if (image.processed) return 'Procesada';
      return 'Pendiente';
    },
    getAverageColorStyle(image) {
      if (!image.analysis_results?.analysis?.average_color) return {};
      const { r, g, b } = image.analysis_results.analysis.average_color;
      return {
        backgroundColor: `rgb(${r}, ${g}, ${b})`
      };
    },
    goBack() {
      this.$router.push({ name: 'proyectos' });
    },
    updateImageAfterProcessing(data) {
      // Actualizar la imagen procesada en el array de imágenes
      if (this.selectedImage && this.project) {
        const imageIndex = this.project.images.findIndex(img => img.id === this.selectedImage.id);
        if (imageIndex !== -1) {
          // Actualizar la imagen con los nuevos datos
          this.project.images[imageIndex] = {
            ...this.project.images[imageIndex],
            processed: true,
            analysis_results: data.results,
            processed_image: data.processed_image_url
          };
          
          // Actualizar la imagen seleccionada
          this.selectedImage = this.project.images[imageIndex];
        }
      }
      // Actualizar estadísticas
      this.loadStatistics();
    },
    updateImageAfterModelGeneration(data) {
      // Actualizar la imagen con los datos 3D generados
      if (this.selectedImage && this.project) {
        const imageIndex = this.project.images.findIndex(img => img.id === this.selectedImage.id);
        if (imageIndex !== -1) {
          // Actualizar la imagen con los nuevos datos 3D
          this.project.images[imageIndex] = {
            ...this.project.images[imageIndex],
            has_3d_data: true,
            data_3d: data.results
          };
          
          // Actualizar la imagen seleccionada
          this.selectedImage = this.project.images[imageIndex];
        }
      }
    },
  }
}
</script>

<style scoped>
.project-detail {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.project-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  background-color: #1a1a1a;
  padding: 1rem 2rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
}

.btn-back {
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 0.5rem 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-right: 1rem;
}

.btn-back:hover {
  background-color: #1a252f;
}

.header-content h1 {
  color: #fff;
  font-size: 2rem;
  margin: 0 0 0.5rem 0;
}

.project-meta {
  display: flex;
  gap: 1.5rem;
  color: #888;
}

.project-meta span {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-upload {
  background: #2196F3;
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.btn-upload:hover {
  background: #1976D2;
}

.project-content {
  display: grid;
  gap: 2rem;
}

.project-info, .project-images, .project-stats {
  background: #1e1e1e;
  border-radius: 10px;
  padding: 1.5rem;
}

.project-info h2, .project-images h2, .project-stats h2 {
  color: #fff;
  margin-bottom: 1rem;
}

.project-info p {
  color: #ccc;
}

.images-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}

.image-card {
  background: #2a2a2a;
  border-radius: 8px;
  overflow: hidden;
}

.image-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.image-info {
  padding: 1rem;
  color: #ccc;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: #2a2a2a;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
}

.stat-card i {
  font-size: 2rem;
  color: #2196F3;
}

.stat-value {
  display: block;
  font-size: 2rem;
  color: #fff;
  margin: 0.5rem 0;
}

.stat-label {
  color: #888;
}

.no-images {
  text-align: center;
  padding: 3rem;
  color: #888;
}

.no-images i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: #1e1e1e;
  padding: 2rem;
  border-radius: 10px;
  width: 90%;
  max-width: 500px;
}

.modal-content h2 {
  color: #fff;
  margin-bottom: 1.5rem;
}

.upload-area {
  border: 2px dashed #666;
  border-radius: 10px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
}

.upload-placeholder {
  color: #888;
}

.upload-placeholder i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.upload-preview {
  margin-top: 1rem;
  text-align: center;
}

.upload-preview img {
  max-width: 100%;
  max-height: 200px;
  border-radius: 5px;
}

.preview-info {
  margin-top: 0.5rem;
  color: #888;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-cancel {
  background: #666;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.loading-content {
  text-align: center;
  color: white;
}

.loading-content i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.error-message {
  text-align: center;
  color: #dc3545;
  padding: 2rem;
}

.error-message i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.image-preview {
  position: relative;
  overflow: hidden;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  opacity: 0;
  transition: opacity 0.3s;
}

.image-preview:hover .image-overlay {
  opacity: 1;
}

.btn-process, .btn-3d, .btn-view {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.btn-process { background: #4CAF50; color: white; }
.btn-3d { background: #2196F3; color: white; }
.btn-view { background: #FFC107; color: black; }

.results-modal {
  width: 90%;
  max-width: 1200px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e0e0e0;
  margin-bottom: 1rem;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #7f8c8d;
}

.btn-close:hover {
  color: #e74c3c;
}

.modal-body {
  max-height: 80vh;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .project-detail {
    padding: 1rem;
  }
  
  .project-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .project-meta {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .btn-upload {
    width: 100%;
    justify-content: center;
  }
}
</style> 