<template>
  <div class="estudio-three">
    <div class="nav-header">
      <button @click="goBackToSistema" class="btn-back">
        <i class="fas fa-arrow-left"></i> Volver al Panel
      </button>
      <h1>Estudio de Modelado 3D</h1>
    </div>
    
    <div class="estudio-container">
      <!-- Panel izquierdo: Selección de imágenes y controles -->
      <div class="panel control-panel">
        <h2>Imágenes del Proyecto</h2>
        
        <!-- Selector de proyecto -->
        <div class="project-selector">
          <select v-model="selectedProjectId" @change="loadProject" class="form-select">
            <option value="">Seleccionar proyecto</option>
            <option v-for="project in projects" :key="project.id" :value="project.id">
              {{ project.name }}
            </option>
          </select>
        </div>
        
        <!-- Lista de imágenes disponibles -->
        <div v-if="projectImages.length > 0" class="image-list">
          <div v-for="image in projectImages" :key="image.id" 
               class="image-item" 
               :class="{ active: selectedImage && selectedImage.id === image.id }"
               @click="selectImage(image)">
            <div class="image-thumb">
              <img :src="image.image" :alt="image.name || 'Imagen'" />
            </div>
            <div class="image-info">
              <div class="image-name">{{ image.name || `Imagen ${image.id}` }}</div>
              <div class="image-date">{{ formatDate(image.uploaded_at) }}</div>
            </div>
          </div>
        </div>
        <div v-else class="no-images">
          No hay imágenes disponibles en este proyecto
        </div>
        
        <!-- Controles de procesamiento -->
        <div class="processing-controls">
          <h2>Procesamiento</h2>
          
          <div class="control-group">
            <label>Método de extracción:</label>
            <select v-model="processingSettings.extractionMethod" class="form-select">
              <option value="contour">Contornos</option>
              <option value="segmentation">Segmentación</option>
              <option value="yolo">YOLO (objetos)</option>
            </select>
          </div>
          
          <div class="control-group">
            <label>Nivel de detalle:</label>
            <div class="range-with-value">
              <input type="range" v-model.number="processingSettings.detailLevel" 
                     min="1" max="10" step="1" class="form-range" />
              <span class="range-value">{{ processingSettings.detailLevel }}</span>
            </div>
          </div>
          
          <div class="control-group">
            <label>Sensibilidad:</label>
            <div class="range-with-value">
              <input type="range" v-model.number="processingSettings.sensitivity" 
                     min="0" max="1" step="0.05" class="form-range" />
              <span class="range-value">{{ processingSettings.sensitivity.toFixed(2) }}</span>
            </div>
          </div>
          
          <div class="action-buttons">
            <button @click="processImage" :disabled="!canProcess" class="btn btn-primary">
              <i class="fas fa-magic"></i> Procesar imagen
            </button>
          </div>
        </div>
      </div>
      
      <!-- Panel central: Visualización de imágenes y resultados 2D -->
      <div class="panel preview-panel">
        <h2>Visualización 2D</h2>
        
        <div class="preview-container">
          <div v-if="selectedImage" class="image-preview">
            <img :src="selectedImage.image" alt="Imagen seleccionada" />
            
            <!-- Overlay para mostrar contornos o segmentación -->
            <canvas ref="overlayCanvas" class="overlay-canvas" v-if="showOverlay"></canvas>
          </div>
          <div v-else-if="processedImageUrl" class="image-preview">
            <img :src="processedImageUrl" alt="Imagen procesada" />
          </div>
          <div v-else class="empty-preview">
            <i class="fas fa-image"></i>
            <p>Selecciona una imagen para procesar</p>
          </div>
        </div>
        
        <!-- Controles de visualización 2D -->
        <div class="visualization-controls">
          <button @click="toggleOverlay" class="btn btn-toggle" :class="{ active: showOverlay }">
            <i class="fas fa-layer-group"></i> Mostrar contornos
          </button>
          <button @click="showOriginal = !showOriginal" class="btn btn-toggle" :class="{ active: showOriginal }">
            <i class="fas fa-eye"></i> Ver original
          </button>
        </div>
      </div>
      
      <!-- Panel derecho: Modelo 3D -->
      <div class="panel model-panel">
        <h2>Modelo 3D</h2>
        
        <div class="model-container">
          <div v-if="modelData" class="model-3d">
            <!-- Aquí irá el visor Three.js -->
            <div ref="threeContainer" class="three-container"></div>
            
            <!-- Overlay para mostrar información del modelo -->
            <div class="model-overlay" v-if="showModelInfo">
              <div class="model-stats">
                <div class="stat-item">
                  <span class="stat-label">Vértices:</span>
                  <span class="stat-value">{{ modelData.metadata ? modelData.metadata.vertices_count.toLocaleString() : '?' }}</span>
                </div>
                <div class="stat-item">
                  <span class="stat-label">Caras:</span>
                  <span class="stat-value">{{ modelData.metadata ? modelData.metadata.faces_count.toLocaleString() : '?' }}</span>
                </div>
                <div class="stat-item" v-if="modelData.metadata && modelData.metadata.image_type">
                  <span class="stat-label">Tipo:</span>
                  <span class="stat-value">{{ modelData.metadata.image_type }}</span>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="empty-model">
            <i class="fas fa-cube"></i>
            <p>Procesa una imagen para generar el modelo 3D</p>
          </div>
        </div>
        
        <!-- Controles del modelo 3D -->
        <div class="model-controls">
          <div class="control-group">
            <label>Exaltación de relieve:</label>
            <div class="range-with-value">
              <input type="range" v-model.number="modelSettings.extrusionScale" 
                     min="0" max="5" step="0.1" class="form-range"
                     @input="updateExtrusionScale" />
              <span class="range-value">{{ modelSettings.extrusionScale.toFixed(1) }}</span>
            </div>
          </div>
          
          <div class="control-group">
            <label>Subdivisión de polígonos:</label>
            <div class="range-with-value">
              <input type="range" v-model.number="modelSettings.subdivisionLevel" 
                     min="0" max="3" step="1" class="form-range"
                     @input="updateSubdivisionLevel" />
              <span class="range-value">{{ modelSettings.subdivisionLevel }}</span>
            </div>
          </div>
          
          <div class="control-group">
            <label>Modo de visualización:</label>
            <div class="render-mode-selector">
              <button 
                @click="setRenderMode('solid')" 
                class="btn btn-toggle" 
                :class="{ active: modelSettings.renderMode === 'solid' }">
                <i class="fas fa-cube"></i>
              </button>
              <button 
                @click="setRenderMode('wireframe')" 
                class="btn btn-toggle" 
                :class="{ active: modelSettings.renderMode === 'wireframe' }">
                <i class="fas fa-vector-square"></i>
              </button>
              <button 
                @click="setRenderMode('points')" 
                class="btn btn-toggle" 
                :class="{ active: modelSettings.renderMode === 'points' }">
                <i class="fas fa-th"></i>
              </button>
              <button 
                @click="setRenderMode('textured')" 
                class="btn btn-toggle" 
                :class="{ active: modelSettings.renderMode === 'textured' }">
                <i class="fas fa-image"></i>
              </button>
            </div>
          </div>
          
          <div class="visualization-options">
            <div class="checkbox-option">
              <input type="checkbox" id="showNormals" v-model="modelSettings.showNormals" @change="toggleNormals">
              <label for="showNormals">Mostrar normales</label>
            </div>
            <div class="checkbox-option">
              <input type="checkbox" id="showModelInfo" v-model="showModelInfo">
              <label for="showModelInfo">Mostrar información</label>
            </div>
            <div class="checkbox-option">
              <input type="checkbox" id="autoRotate" v-model="modelSettings.autoRotate" @change="toggleAutoRotate">
              <label for="autoRotate">Rotación automática</label>
            </div>
          </div>
          
          <div class="action-buttons">
            <button @click="exportModel" :disabled="!modelData" class="btn btn-success">
              <i class="fas fa-file-export"></i> Exportar modelo
            </button>
            <button @click="saveModel" :disabled="!modelData" class="btn btn-primary">
              <i class="fas fa-save"></i> Guardar modelo
            </button>
            <button @click="resetModelView" :disabled="!modelData" class="btn btn-secondary">
              <i class="fas fa-undo"></i> Resetear vista
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFExporter } from 'three/examples/jsm/exporters/GLTFExporter.js';
import { STLExporter } from 'three/examples/jsm/exporters/STLExporter.js';
import { PLYExporter } from 'three/examples/jsm/exporters/PLYExporter.js';
import { OBJExporter } from 'three/examples/jsm/exporters/OBJExporter.js';

// Configuración de axios
const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
});

export default {
  name: 'EstudioThreeView',
  
  data() {
    return {
      // Proyectos e imágenes
      projects: [],
      selectedProjectId: '',
      projectImages: [],
      selectedImage: null,
      
      // Estado de procesamiento
      isProcessing: false,
      processedImageUrl: null,
      showOverlay: false,
      showOriginal: false,
      
      // Configuraciones de procesamiento
      processingSettings: {
        extractionMethod: 'contour',
        detailLevel: 5,
        sensitivity: 0.5
      },
      
      // Datos y configuración del modelo 3D
      modelData: null,
      modelSettings: {
        extrusionScale: 1.0,
        subdivisionLevel: 0,
        renderMode: 'solid',
        showNormals: false,
        autoRotate: false
      },
      showModelInfo: false,
      
      // Objetos Three.js - Marcados como no reactivos      scene: null,      camera: null,      renderer: null,      controls: null,      model: null,      normalsHelper: null,      exportFormat: 'gltf',      animationFrameId: null, // Para controlar y detener la animación
      
      // Objetos para efectos visuales - No reactivos
      materialOptions: null
    };
  },
  
  computed: {
    canProcess() {
      return this.selectedImage && !this.isProcessing;
    }
  },
  
  mounted() {
    this.loadProjects();
  },
  
  methods: {
    // Métodos para cargar datos
    async loadProjects() {
      try {
        const response = await api.get('/api/projects/');
        this.projects = response.data;
      } catch (error) {
        console.error('Error cargando proyectos:', error);
      }
    },
    
    async loadProject() {
      if (!this.selectedProjectId) {
        this.projectImages = [];
        this.selectedImage = null;
        return;
      }
      
      try {
        const response = await api.get(`/api/projects/${this.selectedProjectId}/`);
        this.projectImages = response.data.images || [];
      } catch (error) {
        console.error('Error cargando imágenes del proyecto:', error);
      }
    },
    
    selectImage(image) {
      this.selectedImage = image;
      this.processedImageUrl = null;
      this.modelData = null;
      this.showOverlay = false;
      
      // Limpiar el canvas de overlay
      this.$nextTick(() => {
        const canvas = this.$refs.overlayCanvas;
        if (canvas) {
          const ctx = canvas.getContext('2d');
          ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
      });
    },
    
    // Métodos de procesamiento
    processImage() {
      if (!this.canProcess) return;
      
      this.isProcessing = true;
      
      // Mostrar indicador de carga
      this.showLoadingIndicator();
      
      try {
        // Llamar al backend para procesar la imagen y generar el modelo 3D
        console.log('Enviando solicitud de procesamiento...');
        api.post('/api/process_image/', {
          image_id: this.selectedImage.id,
          pipeline: [
            {
              algorithm: this.processingSettings.extractionMethod, 
              params: {
                detail_level: this.processingSettings.detailLevel,
                sensitivity: this.processingSettings.sensitivity
              }
            }
          ]
        })
        .then(response => {
          console.log('Respuesta recibida:', response.data);
          
          // Actualizar vista con los resultados
          this.processedImageUrl = response.data.processed_image;
          
          // Si la respuesta incluye datos 3D, inicializar el modelo
          if (response.data.model_3d) {
            console.log('Datos 3D recibidos:', response.data.model_3d);
            
            // IMPORTANTE: Desconectar completamente del sistema reactivo de Vue
            // Crear una copia normal (no reactiva) de los datos
            this.modelData = JSON.parse(JSON.stringify(response.data.model_3d));
            
            // Limpiar Three.js completamente antes de reiniciar
            this.cleanupThree();
            
            this.$nextTick(() => {
              console.log('Inicializando escena Three.js...');
              this.initThreeScene();
            });
          } else {
            console.error('No se recibieron datos 3D en la respuesta');
            this.showModelErrorMessage();
          }
          
          // Dibujar los contornos en el overlay si es necesario
          if (response.data.contours) {
            this.drawOverlay(response.data.contours);
          }
          
          this.hideLoadingIndicator();
          this.isProcessing = false;
        })
        .catch(error => {
          console.error('Error procesando imagen:', error);
          this.hideLoadingIndicator();
          this.showModelErrorMessage();
          this.isProcessing = false;
        });
        
      } catch (error) {
        console.error('Error procesando imagen:', error);
        this.hideLoadingIndicator();
        this.showModelErrorMessage();
        this.isProcessing = false;
      }
    },
    
    toggleOverlay() {
      this.showOverlay = !this.showOverlay;
    },
    
    drawOverlay(contours) {
      if (!this.$refs.overlayCanvas) return;
      
      const canvas = this.$refs.overlayCanvas;
      const ctx = canvas.getContext('2d');
      
      // Ajustar el tamaño del canvas al tamaño de la imagen
      const img = new Image();
      img.onload = () => {
        canvas.width = img.width;
        canvas.height = img.height;
        
        // Limpiar el canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Dibujar los contornos
        ctx.strokeStyle = '#00ff00';
        ctx.lineWidth = 2;
        
        for (const contour of contours) {
          ctx.beginPath();
          for (let i = 0; i < contour.length; i++) {
            const point = contour[i];
            if (i === 0) {
              ctx.moveTo(point.x, point.y);
            } else {
              ctx.lineTo(point.x, point.y);
            }
          }
          ctx.closePath();
          ctx.stroke();
        }
      };
      img.src = this.selectedImage.image;
    },
    
    // Métodos Three.js
    initThreeScene() {
      if (!this.$refs.threeContainer) {
        console.error('No se puede inicializar Three.js: Falta contenedor');
        return;
      }
      
      console.log('Iniciando Three.js con contenedor:', this.$refs.threeContainer);
      if (this.modelData) {
        console.log('Datos del modelo:', this.modelData);
      } else {
        console.warn('No hay datos del modelo disponibles');
      }

      const container = this.$refs.threeContainer;
      
      // IMPORTANTE: Evitar problemas de proxy con Three.js
      // Crear objetos fuera de la reactividad de Vue
      // Inicializar Three.js
      const scene = new THREE.Scene();
      scene.background = new THREE.Color(0x111111);
      this.scene = scene;
      
      // Configurar cámara - Crear fuera de la reactividad de Vue
      const camera = new THREE.PerspectiveCamera(
        75, 
        container.clientWidth / container.clientHeight, 
        0.1, 
        1000
      );
      camera.position.z = 5;
      this.camera = camera;
      
      // Configurar renderer con mejoras visuales - Crear fuera de la reactividad
      const renderer = new THREE.WebGLRenderer({ 
        antialias: true,
        alpha: true,
        preserveDrawingBuffer: true,
        logarithmicDepthBuffer: true
      });
      renderer.setSize(container.clientWidth, container.clientHeight);
      renderer.setPixelRatio(window.devicePixelRatio);
      renderer.shadowMap.enabled = true;
      renderer.shadowMap.type = THREE.PCFSoftShadowMap;
      renderer.outputEncoding = THREE.sRGBEncoding;
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      renderer.toneMappingExposure = 1.0;
      container.innerHTML = '';
      container.appendChild(renderer.domElement);
      this.renderer = renderer;
      
      // Añadir controles - No reactivos
      const controls = new OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.05;
      controls.rotateSpeed = 0.7;
      controls.zoomSpeed = 1.2;
      controls.panSpeed = 0.8;
      this.controls = controls;
      
      // Añadir luces mejoradas - No reactivas
      // Luz ambiental
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
      scene.add(ambientLight);
      
      // Luz direccional principal (con sombras)
      const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
      directionalLight.position.set(1, 1, 1);
      directionalLight.castShadow = true;
      directionalLight.shadow.mapSize.width = 2048;
      directionalLight.shadow.mapSize.height = 2048;
      directionalLight.shadow.camera.near = 0.5;
      directionalLight.shadow.camera.far = 500;
      directionalLight.shadow.bias = -0.0001;
      scene.add(directionalLight);
      
      // Luz superior suave
      const topLight = new THREE.DirectionalLight(0xaabbff, 0.4);
      topLight.position.set(0, 1, 0);
      scene.add(topLight);
      
      // Iluminación hemisférica para mejorar detalles
      const hemiLight = new THREE.HemisphereLight(0xbbddff, 0x444466, 0.5);
      hemiLight.position.set(0, 1, 0);
      scene.add(hemiLight);
      
      // Añadir un reflector (spotlight) para mejorar la visualización
      const spotLight = new THREE.SpotLight(0xffffff, 0.5);
      spotLight.position.set(5, 10, 5);
      spotLight.angle = Math.PI / 6;
      spotLight.penumbra = 0.3;
      spotLight.decay = 2;
      spotLight.distance = 30;
      spotLight.castShadow = true;
      scene.add(spotLight);
      
      // Crear materiales con mejor apariencia visual pero NO REACTIVOS
      this.materialOptions = {
        solid: new THREE.MeshPhysicalMaterial({
          vertexColors: true,
          flatShading: true,
          side: THREE.DoubleSide,
          color: 0x3399ff,
          metalness: 0.2,
          roughness: 0.8,
          clearcoat: 0.3,
          clearcoatRoughness: 0.25,
          reflectivity: 1.0
        }),
        wireframe: new THREE.MeshBasicMaterial({
          wireframe: true,
          color: 0x4a9eff,
          side: THREE.DoubleSide
        }),
        points: new THREE.PointsMaterial({
          size: 0.025,
          vertexColors: true,
          sizeAttenuation: true,
          color: 0xffffff
        }),
        textured: new THREE.MeshStandardMaterial({
          vertexColors: true,
          flatShading: false,
          side: THREE.DoubleSide,
          roughness: 0.7,
          metalness: 0.2,
          color: 0x3399ff
        })
      };
      
      // Añadir objetos visuales de ayuda
      // Crear axis helper
      const axesHelper = new THREE.AxesHelper(2);
      scene.add(axesHelper);
      
      // Añadir una cuadrícula para referencia
      const gridHelper = new THREE.GridHelper(10, 20, 0x444466, 0x222233);
      scene.add(gridHelper);
      
      // Crear un fondo con gradiente para mejor percepción de profundidad
      const bgGeometry = new THREE.SphereGeometry(50, 32, 32);
      const bgMaterial = new THREE.ShaderMaterial({
        side: THREE.BackSide,
        uniforms: {
          topColor: { value: new THREE.Color(0x000022) },
          bottomColor: { value: new THREE.Color(0x220011) },
        },
        vertexShader: `
          varying vec3 vWorldPosition;
          void main() {
            vWorldPosition = (modelMatrix * vec4(position, 1.0)).xyz;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
          }
        `,
        fragmentShader: `
          uniform vec3 topColor;
          uniform vec3 bottomColor;
          varying vec3 vWorldPosition;
          void main() {
            float h = normalize(vWorldPosition).y * 0.5 + 0.5;
            gl_FragColor = vec4(mix(bottomColor, topColor, h), 1.0);
          }
        `
      });
      const bgSphere = new THREE.Mesh(bgGeometry, bgMaterial);
      scene.add(bgSphere);
      
      // Si tenemos datos del modelo, crearlos ahora
      if (this.modelData) {
        this.createModel();
      } else {
        // Si no hay modelo, crear un objeto de prueba visualmente atractivo
        this.createTestObject();
      }
      
      // Iniciar el bucle de renderizado usando requestAnimationFrame directamente
      // en lugar de un método de Vue para evitar el contexto de Vue
      const animate = () => {
        // Almacenar el ID de la animación para poder cancelarla más tarde
        this.animationFrameId = requestAnimationFrame(animate);
        
        if (controls) {
          controls.update();
        }
        
        // Rotar el modelo lentamente si autoRotate está activado
        if (this.model && this.modelSettings.autoRotate) {
          this.model.rotation.y += 0.005;
        }
        
        if (this.renderer && this.scene && this.camera) {
          try {
            // Renderizar la escena dentro de un try-catch para capturar errores
            this.renderer.render(this.scene, this.camera);
          } catch (error) {
            console.error('Error en renderizado:', error);
            // Cancelar la animación en caso de error
            cancelAnimationFrame(this.animationFrameId);
            // Mostrar mensaje de error
            this.showModelErrorMessage();
          }
        }
        
        // Actualizar helpers si existen
        if (this.normalsHelper) {
          this.normalsHelper.update();
        }
      };
      
      // Iniciar la animación
      animate();
      
      // Manejar cambios de tamaño
      window.addEventListener('resize', this.onResize);
    },
    
    createModel() {
      if (!this.scene || !this.modelData) {
        console.error('No se puede crear el modelo: faltan datos o escena');
        return;
      }
      
      console.log('Creando geometría del modelo...');
      
      try {
        // Verificar que los datos son arrays válidos
        if (!this.modelData.vertices || !Array.isArray(this.modelData.vertices) || this.modelData.vertices.length === 0) {
          console.error('Datos de vértices inválidos:', this.modelData.vertices);
          
          // Crear un objeto de prueba si no hay datos válidos
          this.createTestObject();
          return;
        }
        
        // Limpiar el modelo anterior y ayudantes si existen
        if (this.model) {
          this.scene.remove(this.model);
          this.model = null;
        }
        
        if (this.normalsHelper) {
          this.scene.remove(this.normalsHelper);
          this.normalsHelper = null;
        }
        
        // Crear geometría a partir de los datos - No reactiva
        const geometry = new THREE.BufferGeometry();
        
        // Añadir vértices - No reactivos
        const vertices = new Float32Array(this.modelData.vertices.flat());
        geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
        
        // Añadir normales si están disponibles - No reactivos
        if (this.modelData.normals && this.modelData.normals.length > 0) {
          const normals = new Float32Array(this.modelData.normals.flat());
          geometry.setAttribute('normal', new THREE.BufferAttribute(normals, 3));
        } else {
          // Calcular normales si no están disponibles
          geometry.computeVertexNormals();
        }
        
        // Añadir colores si están disponibles - No reactivos
        if (this.modelData.colors && this.modelData.colors.length > 0) {
          const colors = new Float32Array(this.modelData.colors.flat());
          geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        }
        
        // Añadir caras - No reactivas
        if (this.modelData.faces && this.modelData.faces.length > 0) {
          const indices = new Uint32Array(this.modelData.faces.flat());
          geometry.setIndex(new THREE.BufferAttribute(indices, 1));
        }
        
        // Aplicar subdivisión si es necesario
        let finalGeometry = geometry;
        if (this.modelSettings.subdivisionLevel > 0) {
          console.log('Aplicando subdivisión nivel:', this.modelSettings.subdivisionLevel);
          finalGeometry = this.applySubdivision(geometry, this.modelSettings.subdivisionLevel);
        }
        
        // Seleccionar el material según el modo de renderizado
        const material = this.materialOptions[this.modelSettings.renderMode];
        
        // Crear la malla o puntos según el modo - No reactivos
        if (this.modelSettings.renderMode === 'points') {
          this.model = new THREE.Points(finalGeometry, material);
        } else {
          this.model = new THREE.Mesh(finalGeometry, material);
          this.model.receiveShadow = true;
          this.model.castShadow = true;
        }
        
        // Aplicar escala de extrusión
        this.model.scale.z = this.modelSettings.extrusionScale;
        
        // Añadir a la escena
        this.scene.add(this.model);
        
        // Mostrar normales si está activado
        this.toggleNormals();
        
        // Centrar la cámara en el modelo
        this.centerCamera();
        
        console.log('Modelo creado con éxito');
      } catch (error) {
        console.error('Error al crear el modelo:', error);
        // Crear un objeto de prueba en caso de error
        this.createTestObject();
      }
    },
    
    applySubdivision(geometry, level) {
      // Implementación simplificada sin usar SubdivisionModifier
      try {
        // Clonar la geometría para preservar la original
        const subdividedGeometry = geometry.clone();
        
        // Convertir a geometría no indexada si es necesario
        if (subdividedGeometry.index) {
          const nonIndexed = subdividedGeometry.toNonIndexed();
          
          // Aplicar suavizado basado en el nivel
          if (level > 0) {
            // Computar normales de vértices para suavizar la apariencia
            nonIndexed.computeVertexNormals();
            
            // Aplicar suavizado proporcional al nivel
            const positions = nonIndexed.getAttribute('position');
            const normals = nonIndexed.getAttribute('normal');
            
            if (positions && normals) {
              const factor = level * 0.05; // Factor de suavizado basado en el nivel
              const posArray = positions.array;
              const normArray = normals.array;
              
              // Mover ligeramente los vértices en la dirección de sus normales
              for (let i = 0; i < posArray.length; i += 3) {
                posArray[i] += normArray[i] * factor;
                posArray[i+1] += normArray[i+1] * factor;
                posArray[i+2] += normArray[i+2] * factor;
              }
              
              positions.needsUpdate = true;
            }
          }
          
          return nonIndexed;
        }
        
        // Si no tiene índices, solo computar normales
        if (level > 0) {
          subdividedGeometry.computeVertexNormals();
        }
        
        return subdividedGeometry;
      } catch (error) {
        console.error('Error al aplicar subdivisión:', error);
        return geometry;  // Devolver geometría original en caso de error
      }
    },
    
    updateExtrusionScale() {
      if (this.model) {
        this.model.scale.z = this.modelSettings.extrusionScale;
      }
    },
    
    updateSubdivisionLevel() {
      // Recrear el modelo con la nueva subdivisión
      this.createModel();
    },
    
    setRenderMode(mode) {
      this.modelSettings.renderMode = mode;
      this.createModel();
    },
    
    toggleNormals() {
      // Eliminar helper existente
      if (this.normalsHelper) {
        this.scene.remove(this.normalsHelper);
        this.normalsHelper = null;
      }
      
      // Crear nuevo helper de normales si está activado - No reactivo
      if (this.modelSettings.showNormals && this.model && this.model.type === 'Mesh') {
        this.normalsHelper = new THREE.VertexNormalsHelper(
          this.model, 
          0.1,  // Longitud
          0x00ff00  // Color
        );
        this.scene.add(this.normalsHelper);
      }
    },
    
    toggleAutoRotate() {
      if (this.controls) {
        this.controls.autoRotate = this.modelSettings.autoRotate;
        this.controls.autoRotateSpeed = 2.0;
      }
    },
    
    resetModelView() {
      if (this.model && this.camera && this.controls) {
        this.centerCamera();
        this.controls.reset();
      }
    },
    
    centerCamera() {
      if (!this.model) return;
      
      // Calcular bounding box
      const box = new THREE.Box3().setFromObject(this.model);
      const center = box.getCenter(new THREE.Vector3());
      const size = box.getSize(new THREE.Vector3());
      
      // Configurar controles y cámara
      this.controls.target.copy(center);
      this.camera.position.copy(center);
      this.camera.position.z += Math.max(size.x, size.y, size.z) * 1.5;
      this.controls.update();
    },
    
    animate() {
      // Este método ya no se usará directamente
      // La animación se hace con una función directa en initThreeScene
      console.warn('Este método animate() ya no se usa. La animación se inicia en initThreeScene');
    },
    
    onResize() {
      if (!this.$refs.threeContainer || !this.camera || !this.renderer) return;
      
      const container = this.$refs.threeContainer;
      
      this.camera.aspect = container.clientWidth / container.clientHeight;
      this.camera.updateProjectionMatrix();
      
      this.renderer.setSize(container.clientWidth, container.clientHeight);
    },
    
    // Métodos para exportar y guardar
    exportModel() {
      if (!this.model) return;
      
      // Crear modal para seleccionar formato
      const format = prompt(
        'Selecciona formato de exportación (gltf, obj, stl, ply):', 
        'gltf'
      );
      
      if (!format) return;
      
      switch(format.toLowerCase()) {
        case 'gltf':
          this.exportGLTF();
          break;
        case 'obj':
          this.exportOBJ();
          break;
        case 'stl':
          this.exportSTL();
          break;
        case 'ply':
          this.exportPLY();
          break;
        default:
          alert('Formato no soportado');
      }
    },
    
    exportGLTF() {
      const exporter = new GLTFExporter();
      const options = {
        binary: false,
        embedImages: true,
        animations: []
      };
      
      exporter.parse(
        this.model,
        (gltf) => {
          const blob = new Blob([JSON.stringify(gltf)], { type: 'application/json' });
          const url = URL.createObjectURL(blob);
          
          const a = document.createElement('a');
          a.href = url;
          a.download = `model_${this.selectedImage.id}.gltf`;
          a.click();
          
          URL.revokeObjectURL(url);
        },
        (error) => {
          console.error('Error exportando modelo GLTF:', error);
          alert('Error al exportar el modelo');
        },
        options
      );
    },
    
    exportSTL() {
      const exporter = new STLExporter();
      const output = exporter.parse(this.model);
      
      const blob = new Blob([output], { type: 'application/octet-stream' });
      const url = URL.createObjectURL(blob);
      
      const a = document.createElement('a');
      a.href = url;
      a.download = `model_${this.selectedImage.id}.stl`;
      a.click();
      
      URL.revokeObjectURL(url);
    },
    
    exportOBJ() {
      const exporter = new OBJExporter();
      const output = exporter.parse(this.model);
      
      const blob = new Blob([output], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      
      const a = document.createElement('a');
      a.href = url;
      a.download = `model_${this.selectedImage.id}.obj`;
      a.click();
      
      URL.revokeObjectURL(url);
    },
    
    exportPLY() {
      const exporter = new PLYExporter();
      
      exporter.parse(
        this.model,
        (output) => {
          const blob = new Blob([output], { type: 'text/plain' });
          const url = URL.createObjectURL(blob);
          
          const a = document.createElement('a');
          a.href = url;
          a.download = `model_${this.selectedImage.id}.ply`;
          a.click();
          
          URL.revokeObjectURL(url);
        },
        { binary: false }
      );
    },
    
    async saveModel() {
      if (!this.modelData || !this.selectedProjectId) return;
      
      try {
        // Actualizar los settings con las configuraciones actuales
        const updatedSettings = {
          ...this.modelData.metadata?.settings || {},
          extrusionScale: this.modelSettings.extrusionScale,
          subdivisionLevel: this.modelSettings.subdivisionLevel,
          renderMode: this.modelSettings.renderMode
        };
        
        await api.post(
          `/api/projects/${this.selectedProjectId}/update_3d_model/`,
          {
            model_data: this.modelData,
            settings: updatedSettings,
            image_id: this.selectedImage.id
          }
        );
        
        alert('Modelo guardado exitosamente');
      } catch (error) {
        console.error('Error guardando modelo:', error);
        alert('Error al guardar el modelo');
      }
    },
    
    // Utilidades
    formatDate(dateString) {
      if (!dateString) return '';
      
      const date = new Date(dateString);
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    },
    
    goBackToSistema() {
      this.$router.push('/sistema');
    },
    
    // Método para crear un objeto de prueba simple para visualización
    createTestObject() {
      console.log('Creando objeto de prueba...');
      
      // Eliminar modelo anterior si existe
      if (this.model) {
        this.scene.remove(this.model);
      }
      
      // Crear una geometría atractiva en lugar de un simple cubo - No reactiva
      const geometry = new THREE.TorusKnotGeometry(1, 0.3, 128, 32);
      
      // Material más atractivo - No reactivo
      const material = new THREE.MeshPhysicalMaterial({ 
        color: 0x3399ff,
        metalness: 0.3,
        roughness: 0.4,
        clearcoat: 0.8,
        clearcoatRoughness: 0.2,
        wireframe: this.modelSettings.renderMode === 'wireframe'
      });
      
      // Crear el objeto y añadirlo a la escena - No reactivo
      this.model = new THREE.Mesh(geometry, material);
      this.model.castShadow = true;
      this.model.receiveShadow = true;
      this.scene.add(this.model);
      
      // Añadir un mensaje visual para informar al usuario
      const message = document.createElement('div');
      message.className = 'model-message';
      message.innerHTML = `
        <div class="message-content">
          <i class="fas fa-exclamation-triangle"></i>
          <p>No se pudo cargar el modelo 3D real.<br>Mostrando objeto de demostración.</p>
        </div>
      `;
      this.$refs.threeContainer.appendChild(message);
      
      // Aplicar rotación para que se vea al iniciar
      this.model.rotation.x = Math.PI / 5;
      this.model.rotation.y = Math.PI / 5;
      
      console.log('Objeto de prueba creado');
    },
    
    showLoadingIndicator() {
      const container = document.createElement('div');
      container.className = 'loading-indicator';
      container.id = 'loadingIndicator';
      container.innerHTML = `
        <div class="spinner"></div>
        <div class="loading-text">Procesando imagen y generando modelo 3D...</div>
      `;
      
      // Agregarlo al contenedor del modelo
      if (this.$refs.threeContainer) {
        this.$refs.threeContainer.appendChild(container);
      }
    },
    
    hideLoadingIndicator() {
      const indicator = document.getElementById('loadingIndicator');
      if (indicator && indicator.parentNode) {
        indicator.parentNode.removeChild(indicator);
      }
    },
    
    showModelErrorMessage() {
      // Crear mensajes de error para el usuario
      if (this.$refs.threeContainer) {
        const message = document.createElement('div');
        message.className = 'error-message';
        message.innerHTML = `
          <div class="message-content">
            <i class="fas fa-exclamation-circle"></i>
            <p>No se pudo generar el modelo 3D.<br>Intenta con otra imagen o ajusta la sensibilidad.</p>
          </div>
        `;
        this.$refs.threeContainer.appendChild(message);
        
        // Crear un objeto de prueba para mostrar algo
        setTimeout(() => {
          this.initThreeScene();
          this.createTestObject();
        }, 500);
      }
    },
    
    cleanupThree() {
      // Almacenar el ID de animación para cancelarlo
      if (this.animationFrameId) {
        cancelAnimationFrame(this.animationFrameId);
        this.animationFrameId = null;
      }
      
      // Eliminar event listeners
      window.removeEventListener('resize', this.onResize);
      
      // Limpiar controles
      if (this.controls) {
        this.controls.dispose();
        this.controls = null;
      }
      
      // Limpiar renderer
      if (this.renderer) {
        this.renderer.dispose();
        this.renderer.forceContextLoss();
        this.renderer.domElement = null;
        this.renderer = null;
      }
      
      // Limpiar modelo
      if (this.model) {
        if (this.model.geometry) this.model.geometry.dispose();
        if (this.model.material) {
          if (Array.isArray(this.model.material)) {
            this.model.material.forEach(m => m.dispose());
          } else {
            this.model.material.dispose();
          }
        }
        this.model = null;
      }
      
      // Limpiar helpers
      if (this.normalsHelper) {
        this.scene.remove(this.normalsHelper);
        this.normalsHelper = null;
      }
      
      // Limpiar escena
      if (this.scene) {
        this.scene.traverse(object => {
          if (object.geometry) object.geometry.dispose();
          if (object.material) {
            if (Array.isArray(object.material)) {
              object.material.forEach(m => m.dispose());
            } else {
              object.material.dispose();
            }
          }
        });
        this.scene = null;
      }
      
      // Liberar memoria de otros objetos
      this.camera = null;
      this.materialOptions = null;
      
      // Limpiar container
      if (this.$refs.threeContainer) {
        this.$refs.threeContainer.innerHTML = '';
      }
    },
    
    beforeUnmount() {
      // Asegurarse de limpiar todo antes de desmontar
      this.cleanupThree();
    }
  },
  
  beforeUnmount() {
    this.cleanupThree();
  }
};
</script>

<style scoped>
.estudio-three {
  margin-top: -60px;
  color: #fff;
  padding: 20px;
  min-height: 100vh;
  background-color: #121212;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.nav-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  background-color: #1e1e1e;
  
  padding: 15px 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.btn-back {
  background-color: #2389da;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 8px 16px;
  margin-right: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.btn-back:hover {
  background-color: #1c75bc;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.nav-header h1 {
  margin: 0;
  color: #a3c9e2;
  font-size: 1.8rem;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.estudio-container {
  display: grid;
  grid-template-columns: 300px 1fr 300px;
  gap: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.panel {
  background: linear-gradient(145deg, #1a2130, #212940);
  border-radius: 12px;
  padding: 20px;
  color: #eee;
  height: calc(100vh - 140px);
  overflow-y: auto;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  border: 1px solid #2d3a4b;
}

h2 {
  font-size: 1.3rem;
  margin-bottom: 15px;
  color: #a3c9e2;
  border-bottom: 1px solid #2d3a4b;
  padding-bottom: 12px;
  font-weight: 600;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
}

.project-selector {
  margin-bottom: 20px;
}

.form-select {
  width: 100%;
  padding: 10px 12px;
  background: #2d3a4b;
  color: white;
  border: 1px solid #3e4d62;
  border-radius: 8px;
  margin-bottom: 15px;
  font-size: 14px;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23a3c9e2' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-position: right 12px center;
  background-repeat: no-repeat;
  background-size: 16px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-select:hover {
  border-color: #5e7d9a;
}

.form-select:focus {
  outline: none;
  border-color: #2389da;
  box-shadow: 0 0 0 3px rgba(35, 137, 218, 0.2);
}

.image-list {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 20px;
  scrollbar-width: thin;
  scrollbar-color: #2d3a4b #1a2130;
}

.image-list::-webkit-scrollbar {
  width: 8px;
}

.image-list::-webkit-scrollbar-track {
  background: #1a2130;
  border-radius: 4px;
}

.image-list::-webkit-scrollbar-thumb {
  background: #2d3a4b;
  border-radius: 4px;
}

.image-list::-webkit-scrollbar-thumb:hover {
  background: #3e4d62;
}

.image-item {
  display: flex;
  align-items: center;
  padding: 12px;
  background: #2d3a4b;
  border-radius: 8px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.image-item:hover {
  background: #3e4d62;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.image-item.active {
  background: #2389da;
  border-color: #a3c9e2;
  box-shadow: 0 4px 12px rgba(35, 137, 218, 0.4);
}

.image-thumb {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  overflow: hidden;
  margin-right: 12px;
  background: #1a1a1a;
  border: 2px solid #3e4d62;
}

.image-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.image-item:hover .image-thumb img {
  transform: scale(1.1);
}

.image-info {
  flex: 1;
}

.image-name {
  font-weight: 600;
  margin-bottom: 4px;
  color: #fff;
}

.image-date {
  font-size: 12px;
  color: #a3c9e2;
}

.processing-controls {
  margin-top: 20px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 15px;
  border: 1px solid #2d3a4b;
}

.control-group {
  margin-bottom: 18px;
}

.control-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  color: #a3c9e2;
  font-weight: 500;
}

.range-with-value {
  display: flex;
  align-items: center;
  gap: 12px;
}

.form-range {
  flex: 1;
  -webkit-appearance: none;
  height: 6px;
  background: #2d3a4b;
  border-radius: 3px;
  cursor: pointer;
}

.form-range::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: #2389da;
  cursor: pointer;
  border: 2px solid #a3c9e2;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  transition: transform 0.1s;
}

.form-range::-webkit-slider-thumb:hover {
  transform: scale(1.2);
}

.range-value {
  min-width: 45px;
  font-size: 14px;
  color: #fff;
  background: #2d3a4b;
  padding: 4px 8px;
  border-radius: 4px;
  text-align: center;
}

.btn {
  background: #2d3a4b;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 8px;
  cursor: pointer;
  margin-right: 8px;
  margin-bottom: 8px;
  font-size: 14px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
  border: 1px solid transparent;
  font-weight: 500;
}

.btn:hover {
  background: #3e4d62;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.btn:disabled {
  background: #1e2836;
  color: #546278;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
  opacity: 0.7;
}

.btn-primary {
  background: #2389da;
  border-color: #5e7d9a;
}

.btn-primary:hover {
  background: #1c75bc;
  border-color: #a3c9e2;
}

.btn-success {
  background: #28a745;
  border-color: #1f8838;
}

.btn-success:hover {
  background: #218838;
  border-color: #6acd8c;
}

.btn-toggle {
  background: #2d3a4b;
  transition: all 0.2s;
  position: relative;
  overflow: hidden;
}

.btn-toggle.active {
  background: #2389da;
}

.btn-toggle:before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 70%);
  transform: scale(0);
  transition: transform 0.3s;
  pointer-events: none;
}

.btn-toggle:active:before {
  transform: scale(2);
}

.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 20px;
}

.preview-container {
  width: 100%;
  height: 400px;
  background: #181818;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  margin-bottom: 15px;
  border: 1px solid #2d3a4b;
  box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.5);
}

.image-preview {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.image-preview img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.overlay-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.empty-preview {
  color: #546278;
  text-align: center;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.empty-preview i {
  font-size: 60px;
  color: #2d3a4b;
  opacity: 0.7;
}

.visualization-controls {
  display: flex;
  gap: 12px;
  margin-bottom: 15px;
}

.model-container {
  width: 100%;
  height: 300px;
  background: #181818;
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 15px;
  border: 1px solid #2d3a4b;
  box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.5);
}

.model-3d {
  width: 100%;
  height: 100%;
}

.three-container {
  width: 100%;
  height: 100%;
  position: relative;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: inset 0 0 40px rgba(0, 0, 0, 0.5);
  transition: all 0.3s ease;
}

.three-container:hover {
  box-shadow: inset 0 0 60px rgba(35, 137, 218, 0.3);
}

.empty-model {
  color: #546278;
  text-align: center;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: 20px;
}

.empty-model i {
  font-size: 60px;
  color: #2d3a4b;
  opacity: 0.7;
}

.model-controls {
  margin-top: 20px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 15px;
  border: 1px solid #2d3a4b;
}

.no-images {
  text-align: center;
  color: #546278;
  padding: 30px 20px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  margin: 10px 0;
}

/* Loading indicator */
.loading-indicator {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #fff;
  border-radius: 10px;
  z-index: 100;
  backdrop-filter: blur(5px);
}

.loading-indicator .spinner {
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  border-top: 4px solid #2389da;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
  box-shadow: 0 0 20px rgba(35, 137, 218, 0.6);
}

.loading-indicator .loading-text {
  font-size: 16px;
  text-align: center;
  color: #a3c9e2;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  max-width: 80%;
}

.error-message,
.model-message {
  position: absolute;
  bottom: 20px;
  left: 20px;
  right: 20px;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 8px;
  padding: 12px 16px;
  color: #fff;
  z-index: 50;
  border-left: 4px solid;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(3px);
}

.error-message {
  border-color: #ff5555;
}

.model-message {
  border-color: #ffbb33;
}

.message-content {
  display: flex;
  align-items: center;
  gap: 15px;
}

.message-content i {
  font-size: 24px;
  color: #ff5555;
}

.model-message .message-content i {
  color: #ffbb33;
}

.message-content p {
  margin: 0;
  font-size: 14px;
  line-height: 1.4;
}

/* Responsive styles */
@media (max-width: 1024px) {
  .estudio-container {
    grid-template-columns: 1fr 1fr;
    grid-template-rows: auto auto;
  }
  
  .control-panel {
    grid-column: 1;
    grid-row: 1;
  }
  
  .preview-panel {
    grid-column: 2;
    grid-row: 1;
  }
  
  .model-panel {
    grid-column: span 2;
    grid-row: 2;
  }
}

@media (max-width: 768px) {
  .estudio-container {
    grid-template-columns: 1fr;
    grid-template-rows: auto auto auto;
  }
  
  .control-panel {
    grid-column: 1;
    grid-row: 1;
  }
  
  .preview-panel {
    grid-column: 1;
    grid-row: 2;
  }
  
  .model-panel {
    grid-column: 1;
    grid-row: 3;
  }
  
  .nav-header {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }
  
  .btn-back {
    margin-right: 0;
    width: 100%;
    justify-content: center;
  }
}

.model-overlay {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 8px;
  padding: 10px;
  color: #fff;
  font-size: 12px;
  z-index: 100;
  pointer-events: none;
}

.model-stats {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.stat-label {
  color: #a3c9e2;
  font-weight: 600;
}

.stat-value {
  color: white;
}

.render-mode-selector {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.render-mode-selector .btn {
  flex: 1;
  justify-content: center;
  padding: 8px 10px;
}

.checkbox-option {
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.checkbox-option input[type="checkbox"] {
  appearance: none;
  width: 18px;
  height: 18px;
  background: #2d3a4b;
  border: 2px solid #3e4d62;
  border-radius: 4px;
  cursor: pointer;
  position: relative;
  transition: all 0.2s;
}

.checkbox-option input[type="checkbox"]:checked {
  background: #2389da;
  border-color: #a3c9e2;
}

.checkbox-option input[type="checkbox"]:checked::after {
  content: '✓';
  position: absolute;
  color: white;
  font-size: 14px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.checkbox-option label {
  font-size: 14px;
  cursor: pointer;
  user-select: none;
}

.visualization-options {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 15px;
  border: 1px solid #2d3a4b;
}

.btn-secondary {
  background: #6c757d;
  border-color: #5a6268;
}

.btn-secondary:hover {
  background: #5a6268;
  border-color: #4e555b;
}

/* Mejorar animación de spinner */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Efectos de hover para controles 3D */
.model-controls .control-group:hover {
  background: rgba(35, 137, 218, 0.1);
  border-radius: 8px;
  transition: background 0.2s;
}

/* Efectos para el estado activo de los controles del modelo */
.model-panel .model-controls .btn.active {
  box-shadow: 0 0 15px rgba(35, 137, 218, 0.5);
  transform: translateY(-3px);
}
</style> 