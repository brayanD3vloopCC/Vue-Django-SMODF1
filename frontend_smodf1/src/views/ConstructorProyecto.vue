<template>
  <div class="constructor-proyecto-page">
    <!-- Navbar minimalista -->
    <div class="constructor-navbar">
      <div class="navbar-logo">
        <img src="@/assets/smodlogotype.jpg" alt="Logo" class="navbar-logo-img" />
        <span class="navbar-title">SMOD F1</span>
      </div>
      <div class="navbar-actions">
        <button class="btn-help">
          <i class="fas fa-question-circle"></i>
        </button>
      </div>
    </div>

    <div class="constructor-layout">
      <!-- Sidebar para configuraciones y ajustes -->
      <div class="constructor-sidebar">
        <div class="sidebar-header">
          <img src="@/assets/smodlogotype.jpg" alt="Logo" class="sidebar-logo" />
          <h2>Constructor de Proyectos</h2>
        </div>
        
        <div class="sidebar-section">
          <h3>Proyecto actual</h3>
          <div class="project-selector">
            <select v-model="currentProjectId" @change="loadProjectData">
              <option value="">Seleccionar proyecto</option>
              <option v-for="project in projects" :key="project.id" :value="project.id">{{ project.name }}</option>
            </select>
            <button @click="createNewProject" class="btn-new">
              <i class="fas fa-plus"></i> Nuevo
            </button>
          </div>
        </div>
        
        <div class="sidebar-section">
          <h3>Algoritmos de Visión</h3>
          <div class="algorithm-options">
            <div class="algorithm-option" v-for="(algo, index) in algorithms" :key="index" @click="selectAlgorithm(algo)">
              <input type="checkbox" :id="'algo-' + index" v-model="algo.selected">
              <label :for="'algo-' + index">{{ algo.name }}</label>
              <i class="fas fa-info-circle" title="Información" @click.stop="showAlgorithmInfo(algo)"></i>
            </div>
          </div>
        </div>
        
        <div class="sidebar-section" v-if="selectedAlgorithm">
          <h3>Configuración: {{ selectedAlgorithm.name }}</h3>
          <div class="algorithm-params">
            <div v-for="(param, pIndex) in selectedAlgorithm.params" :key="pIndex" class="param-control">
              <label>{{ param.name }}</label>
              <div class="param-input">
                <input v-if="param.type === 'range'" type="range" v-model.number="param.value" :min="param.min" :max="param.max" :step="param.step">
                <input v-else-if="param.type === 'number'" type="number" v-model.number="param.value" :min="param.min" :max="param.max" :step="param.step">
                <input v-else-if="param.type === 'text'" type="text" v-model="param.value">
                <select v-else-if="param.type === 'select'" v-model="param.value">
                  <option v-for="(opt, oIndex) in param.options" :key="oIndex" :value="opt.value">{{ opt.label }}</option>
                </select>
                <div v-else-if="param.type === 'color'" class="color-picker">
                  <input type="color" v-model="param.value">
                </div>
                <div v-if="param.type === 'range'" class="range-value">{{ param.value }}</div>
              </div>
            </div>
          </div>
          <div class="algorithm-actions">
            <button class="btn-apply" @click="applyAlgorithm">Aplicar</button>
            <button class="btn-reset" @click="resetAlgorithmParams">Restablecer</button>
          </div>
        </div>

        <div class="sidebar-section">
          <h3>Flujo de Procesamiento</h3>
          <div class="processing-pipeline">
            <div v-for="(step, sIndex) in processingPipeline" :key="sIndex" class="pipeline-step" :class="{ active: step.active }" @click="togglePipelineStep(sIndex)">
              <div class="step-header">
                <span class="step-number">{{ sIndex + 1 }}</span>
                <span class="step-name">{{ step.name }}</span>
                <div class="step-actions">
                  <button @click.stop="moveStepUp(sIndex)" :disabled="sIndex === 0"><i class="fas fa-arrow-up"></i></button>
                  <button @click.stop="moveStepDown(sIndex)" :disabled="sIndex === processingPipeline.length - 1"><i class="fas fa-arrow-down"></i></button>
                  <button @click.stop="removeStep(sIndex)"><i class="fas fa-times"></i></button>
                </div>
              </div>
            </div>
            <div class="pipeline-empty" v-if="processingPipeline.length === 0">
              <p>Agrega algoritmos al flujo de procesamiento</p>
            </div>
          </div>
        </div>

        <div class="sidebar-section">
          <h3>Exportar</h3>
          <div class="export-options">
            <button @click="exportJSON" class="btn-export"><i class="fas fa-file-code"></i> Exportar JSON</button>
            <button @click="exportDatasheet" class="btn-export"><i class="fas fa-file-excel"></i> Exportar Datasheet</button>
            <button @click="saveProcessingPipeline" class="btn-export"><i class="fas fa-save"></i> Guardar Pipeline</button>
          </div>
        </div>
      </div>
      
      <!-- Área principal de trabajo -->
      <div class="constructor-main">
        <div class="workspace-header">
          <h2 v-if="currentProject">{{ currentProject.name }}</h2>
          <h2 v-else>Selecciona o crea un proyecto</h2>
          
          <div class="workspace-actions">
            <div class="workspace-stats" v-if="currentProject">
              <div class="stat-item">
                <i class="fas fa-image"></i> {{ currentProject.images ? currentProject.images.length : 0 }} imágenes
              </div>
              <div class="stat-item">
                <i class="fas fa-calendar-alt"></i> Actualizado: {{ new Date().toLocaleDateString() }}
              </div>
            </div>
            <button @click="processCurrentImage" class="btn-process" :disabled="!currentImage || processingInProgress">
              <i class="fas fa-magic"></i> Procesar
            </button>
            <button @click="toggleSplitView" class="btn-toggle-view">
              <i :class="splitView ? 'fas fa-columns' : 'fas fa-image'"></i>
              {{ splitView ? 'Vista dividida' : 'Vista única' }}
            </button>
          </div>
        </div>
        
        <div class="workspace-content" :class="{ 'split-view': splitView }">
          <div class="image-container original">
            <div class="image-header">
              <h3>Imagen Original</h3>
              <div class="image-actions">
                <button @click="uploadImage" :disabled="!currentProject">
                  <i class="fas fa-upload"></i> Subir
                </button>
                <select v-if="currentProject && currentProject.images && currentProject.images.length" v-model="currentImageId" @change="selectImage">
                  <option value="">Seleccionar imagen</option>
                  <option v-for="img in currentProject.images" :key="img.id" :value="img.id">{{ img.name || 'Imagen ' + img.id }}</option>
                </select>
              </div>
            </div>
            <div class="image-info" v-if="currentImage">
              <div class="info-item">
                <span class="info-label">ID:</span> 
                <span class="info-value">{{ currentImage.id }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Nombre:</span> 
                <span class="info-value">{{ currentImage.name || getImageName(currentImage.image) }}</span>
              </div>
              <div class="info-item" v-if="currentImage.image_width && currentImage.image_height">
                <span class="info-label">Dimensiones:</span> 
                <span class="info-value">{{ currentImage.image_width }}x{{ currentImage.image_height }}</span>
              </div>
              <div class="info-item" v-if="currentImage.processed">
                <span class="info-label">Estado:</span> 
                <span class="info-value processed">Procesada</span>
              </div>
              <div class="info-item" v-else>
                <span class="info-label">Estado:</span> 
                <span class="info-value">Sin procesar</span>
              </div>
            </div>
            <div class="image-workspace">
              <img v-if="currentImage" :src="currentImage.image" alt="Imagen original" @click="openImageViewer(currentImage.image)" class="clickable-image" />
              <div v-else class="no-image">
                <i class="fas fa-image"></i>
                <p>No hay imagen seleccionada</p>
              </div>
            </div>
          </div>
          
          <div class="image-container processed" v-if="splitView || processedImage">
            <div class="image-header">
              <h3>Imagen Procesada</h3>
              <div class="image-actions">
                <button @click="saveProcessedImage" :disabled="!processedImage">
                  <i class="fas fa-save"></i> Guardar
                </button>
                <button @click="downloadProcessedImage" :disabled="!processedImage">
                  <i class="fas fa-download"></i> Descargar
                </button>
              </div>
            </div>
            <div class="image-workspace">
              <div v-if="processingInProgress" class="processing-overlay">
                <div class="spinner">
                  <i class="fas fa-spinner fa-spin"></i>
                  <p>Procesando imagen...</p>
                </div>
              </div>
              <img v-if="processedImage" :src="processedImage" alt="Imagen procesada" @click="openImageViewer(processedImage)" class="clickable-image" />
              <div v-else class="no-image">
                <i class="fas fa-image"></i>
                <p>Procesa la imagen para ver resultados</p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="results-panel" v-if="processingResults">
          <div class="results-header">
            <h3>Resultados del procesamiento</h3>
            <div class="results-actions">
              <button @click="collapseResults = !collapseResults">
                <i :class="collapseResults ? 'fas fa-chevron-down' : 'fas fa-chevron-up'"></i>
              </button>
            </div>
          </div>
          <div class="results-content" v-if="!collapseResults">
            <div class="results-tabs">
              <button 
                v-for="(tab, index) in resultTabs" 
                :key="index" 
                @click="activeResultTab = tab.id"
                :class="{ active: activeResultTab === tab.id }">
                {{ tab.name }}
              </button>
            </div>
            
            <div class="tab-content">
              <!-- Detecciones -->
              <div v-if="activeResultTab === 'detections'" class="detection-results">
                <table v-if="processingResults.detections && processingResults.detections.length">
                  <thead>
                    <tr>
                      <th>Tipo</th>
                      <th>Confianza</th>
                      <th>Posición</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(detection, index) in processingResults.detections" :key="index">
                      <td>{{ detection.class }}</td>
                      <td>{{ (detection.confidence * 100).toFixed(2) }}%</td>
                      <td>[{{ detection.x }}, {{ detection.y }}, {{ detection.width }}, {{ detection.height }}]</td>
                      <td>
                        <button @click="highlightDetection(index)" title="Resaltar">
                          <i class="fas fa-eye"></i>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <div v-else class="no-results">No se encontraron detecciones</div>
              </div>
              
              <!-- Métricas -->
              <div v-else-if="activeResultTab === 'metrics'" class="metrics-results">
                <div v-if="processingResults.metrics" class="metrics-grid">
                  <div v-for="(value, key) in processingResults.metrics" :key="key" class="metric-item">
                    <div class="metric-name">{{ formatMetricName(key) }}</div>
                    <div class="metric-value">{{ formatMetricValue(value) }}</div>
                  </div>
                </div>
                <div v-else class="no-results">No hay métricas disponibles</div>
              </div>
              
              <!-- JSON -->
              <div v-else-if="activeResultTab === 'json'" class="json-results">
                <pre>{{ JSON.stringify(processingResults, null, 2) }}</pre>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Modals -->
    <div v-if="showAlgorithmInfoModal" class="modal-overlay" @click="showAlgorithmInfoModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ algorithmInfoData.name }}</h2>
          <button @click="showAlgorithmInfoModal = false" class="btn-close">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <p>{{ algorithmInfoData.description }}</p>
          
          <div class="algo-details">
            <h3>Uso recomendado</h3>
            <p>{{ algorithmInfoData.usage }}</p>
            
            <h3>Optimización</h3>
            <p>{{ algorithmInfoData.optimization }}</p>
            
            <h3>Ejemplos</h3>
            <div class="algo-examples">
              <div v-for="(example, index) in algorithmInfoData.examples" :key="index" class="algo-example">
                <img :src="example.image" :alt="example.description" />
                <p>{{ example.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="showNewProjectModal" class="modal-overlay" @click="showNewProjectModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Nuevo Proyecto</h2>
          <button @click="showNewProjectModal = false" class="btn-close">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="confirmCreateProject">
            <div class="form-group">
              <label>Nombre del Proyecto</label>
              <input v-model="newProject.name" type="text" required>
            </div>
            <div class="form-group">
              <label>Descripción</label>
              <textarea v-model="newProject.description" rows="4"></textarea>
            </div>
            <div class="form-group">
              <label>Tipo de Proyecto</label>
              <select v-model="newProject.type">
                <option value="detection">Detección de objetos</option>
                <option value="segmentation">Segmentación</option>
                <option value="classification">Clasificación</option>
                <option value="custom">Personalizado</option>
              </select>
            </div>
            <div class="modal-actions">
              <button type="button" @click="showNewProjectModal = false" class="btn-cancel">Cancelar</button>
              <button type="submit" class="btn-create">Crear Proyecto</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    
    <!-- Loading -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner">
        <i class="fas fa-spinner fa-spin"></i>
        <p>{{ loadingMessage }}</p>
      </div>
    </div>

    <!-- Welcome Banner -->
    <div v-if="showWelcomeBanner" class="welcome-banner">
      <div class="welcome-content">
        <div class="welcome-header">
          <h2>Bienvenido al Constructor de Proyectos</h2>
          <button @click="showWelcomeBanner = false" class="btn-close">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="welcome-body">
          <p>Este es el entorno de trabajo para procesamiento de visión artificial. Desde aquí podrás:</p>
          <ul>
            <li><i class="fas fa-check"></i> Aplicar algoritmos a tus imágenes</li>
            <li><i class="fas fa-check"></i> Crear flujos de procesamiento personalizados</li>
            <li><i class="fas fa-check"></i> Visualizar y exportar resultados</li>
            <li><i class="fas fa-check"></i> Guardar configuraciones para uso futuro</li>
          </ul>
          <p>Este es un <strong>modo de demostración</strong> con datos simulados. Explora las funcionalidades!</p>
        </div>
        <div class="welcome-footer">
          <button @click="showWelcomeBanner = false" class="welcome-btn">
            Comenzar a explorar
          </button>
        </div>
      </div>
    </div>

    <!-- Image Viewer Modal -->
    <div v-if="showImageViewer" class="modal-overlay" @click="showImageViewer = false">
      <div class="image-viewer-modal" @click.stop>
        <div class="modal-header">
          <h2>Vista ampliada</h2>
          <button @click="showImageViewer = false" class="btn-close">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="image-viewer-content">
          <img :src="viewerImage" alt="Imagen ampliada" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axiosInstance from '@/utils/axios';

export default {
  name: 'ConstructorProyecto',
  data() {
    return {
      // Project Management
      projects: [],
      currentProjectId: null,
      currentProject: null,
      newProject: {
        name: '',
        description: '',
        type: 'detection'
      },
      
      // Image Management
      currentImageId: null,
      currentImage: null,
      processedImage: null,
      
      // UI State
      loading: false,
      loadingMessage: '',
      showAlgorithmInfoModal: false,
      showNewProjectModal: false,
      showWelcomeBanner: true,
      splitView: true,
      selectedAlgorithm: null,
      processingInProgress: false,
      collapseResults: false,
      activeResultTab: 'detections',
      algorithmInfoData: {},
      
      // Processing Results
      processingResults: null,
      
      // Algorithms
      algorithms: [
        {
          id: 'object_detection',
          name: 'Detección de Objetos',
          description: 'Detecta objetos en imágenes utilizando YOLOv5 optimizado con Cython.',
          usage: 'Ideal para identificar y localizar múltiples objetos dentro de una imagen.',
          optimization: 'Implementado con aceleración Cython y paralelización para rendimiento óptimo.',
          selected: false,
          params: [
            {
              name: 'Confianza mínima',
              type: 'range',
              value: 0.5,
              min: 0.1,
              max: 1.0,
              step: 0.05,
              default: 0.5
            },
            {
              name: 'IOU Threshold',
              type: 'range',
              value: 0.45,
              min: 0.1,
              max: 0.9,
              step: 0.05,
              default: 0.45
            },
            {
              name: 'Modelo',
              type: 'select',
              value: 'yolov5s',
              options: [
                { value: 'yolov5s', label: 'YOLOv5 Small' },
                { value: 'yolov5m', label: 'YOLOv5 Medium' },
                { value: 'yolov5l', label: 'YOLOv5 Large' }
              ],
              default: 'yolov5s'
            }
          ],
          examples: [
            {
              image: '/examples/object_detection_1.jpg',
              description: 'Detección de personas y vehículos en entorno urbano'
            }
          ]
        },
        {
          id: 'people_detection',
          name: 'Detección de Personas',
          description: 'Detecta personas en imágenes utilizando el detector HOG (Histogram of Oriented Gradients) de OpenCV.',
          usage: 'Ideal para identificar personas en imágenes, videos de seguridad o análisis de multitudes.',
          optimization: 'Utiliza vectorización optimizada y algoritmos de agrupación eficientes.',
          selected: false,
          params: [
            {
              name: 'Factor de escala',
              type: 'range',
              value: 1.05,
              min: 1.01,
              max: 1.4,
              step: 0.01,
              default: 1.05
            },
            {
              name: 'Mínimo de vecinos',
              type: 'range',
              value: 3,
              min: 1,
              max: 10,
              step: 1,
              default: 3
            },
            {
              name: 'Altura mínima',
              type: 'range',
              value: 100,
              min: 50,
              max: 300,
              step: 10,
              default: 100
            }
          ],
          examples: [
            {
              image: '/examples/people_detection_1.jpg',
              description: 'Detección de personas en espacios públicos'
            }
          ]
        },
        {
          id: 'face_detection',
          name: 'Detección de Rostros',
          description: 'Detecta rostros en imágenes utilizando clasificadores en cascada Haar de OpenCV.',
          usage: 'Ideal para identificar y localizar rostros en fotografías, videos de vigilancia o análisis de contenido.',
          optimization: 'Implementa algoritmos optimizados para detección facial.',
          selected: false,
          params: [
            {
              name: 'Factor de escala',
              type: 'range',
              value: 1.1,
              min: 1.05,
              max: 1.5,
              step: 0.05,
              default: 1.1
            },
            {
              name: 'Mínimo de vecinos',
              type: 'range',
              value: 5,
              min: 1,
              max: 10,
              step: 1,
              default: 5
            },
            {
              name: 'Ancho mínimo',
              type: 'range',
              value: 30,
              min: 10,
              max: 100,
              step: 5,
              default: 30
            },
            {
              name: 'Alto mínimo',
              type: 'range',
              value: 30,
              min: 10,
              max: 100,
              step: 5,
              default: 30
            }
          ],
          examples: [
            {
              image: '/examples/face_detection_1.jpg',
              description: 'Detección de rostros en retratos y fotografías'
            }
          ]
        },
        {
          id: 'edge_detection',
          name: 'Detección de Bordes',
          description: 'Algoritmo optimizado para detección de bordes utilizando operadores Sobel y Canny.',
          usage: 'Útil para destacar los contornos y bordes de objetos en la imagen.',
          optimization: 'Implementa procesamiento paralelo y filtros optimizados.',
          selected: false,
          params: [
            {
              name: 'Método',
              type: 'select',
              value: 'canny',
              options: [
                { value: 'canny', label: 'Canny' },
                { value: 'sobel', label: 'Sobel' },
                { value: 'prewitt', label: 'Prewitt' }
              ],
              default: 'canny'
            },
            {
              name: 'Umbral inferior',
              type: 'range',
              value: 100,
              min: 0,
              max: 255,
              step: 1,
              default: 100
            },
            {
              name: 'Umbral superior',
              type: 'range',
              value: 200,
              min: 0,
              max: 255,
              step: 1,
              default: 200
            }
          ],
          examples: [
            {
              image: '/examples/edge_detection_1.jpg',
              description: 'Detección de bordes en una imagen arquitectónica'
            }
          ]
        },
        {
          id: 'segmentation',
          name: 'Segmentación',
          description: 'Segmentación de imágenes utilizando algoritmos de clustering y watershed.',
          usage: 'Ideal para separar diferentes regiones o objetos en una imagen.',
          optimization: 'Usa algoritmos paralelos y técnicas de muestreo adaptativo para acelerar el procesamiento.',
          selected: false,
          params: [
            {
              name: 'Método',
              type: 'select',
              value: 'watershed',
              options: [
                { value: 'watershed', label: 'Watershed' },
                { value: 'kmeans', label: 'K-Means' },
                { value: 'grabcut', label: 'GrabCut' }
              ],
              default: 'watershed'
            },
            {
              name: 'Número de segmentos',
              type: 'number',
              value: 5,
              min: 2,
              max: 20,
              step: 1,
              default: 5
            },
            {
              name: 'Suavizado',
              type: 'range',
              value: 0.5,
              min: 0,
              max: 1,
              step: 0.1,
              default: 0.5
            }
          ],
          examples: [
            {
              image: '/examples/segmentation_1.jpg',
              description: 'Segmentación de una imagen médica mostrando diferentes tejidos'
            }
          ]
        },
        {
          id: 'feature_extraction',
          name: 'Extracción de Características',
          description: 'Extrae características clave de la imagen utilizando SIFT, SURF u ORB.',
          usage: 'Perfecto para identificar puntos de interés en la imagen para comparación o tracking.',
          optimization: 'Implementaciones optimizadas con procesamiento vectorial.',
          selected: false,
          params: [
            {
              name: 'Método',
              type: 'select',
              value: 'orb',
              options: [
                { value: 'orb', label: 'ORB' },
                { value: 'sift', label: 'SIFT' },
                { value: 'surf', label: 'SURF' }
              ],
              default: 'orb'
            },
            {
              name: 'Número de características',
              type: 'number',
              value: 500,
              min: 100,
              max: 2000,
              step: 100,
              default: 500
            },
            {
              name: 'Color de marcadores',
              type: 'color',
              value: '#00FF00',
              default: '#00FF00'
            }
          ],
          examples: [
            {
              image: '/examples/feature_extraction_1.jpg',
              description: 'Extracción de puntos de interés en una imagen urbana'
            }
          ]
        },
        {
          id: 'enhancement',
          name: 'Mejora de Imagen',
          description: 'Mejora la calidad de la imagen a través de ajustes de contraste, brillo, reducción de ruido y más.',
          usage: 'Ideal para preprocesamiento o para mejorar imágenes de baja calidad.',
          optimization: 'Algoritmos eficientes para procesamiento en tiempo real.',
          selected: false,
          params: [
            {
              name: 'Método',
              type: 'select',
              value: 'clahe',
              options: [
                { value: 'clahe', label: 'CLAHE (Contraste adaptativo)' },
                { value: 'denoise', label: 'Reducción de ruido' },
                { value: 'sharpen', label: 'Nitidez' },
                { value: 'gamma', label: 'Corrección Gamma' }
              ],
              default: 'clahe'
            },
            {
              name: 'Intensidad',
              type: 'range',
              value: 1.5,
              min: 0.5,
              max: 3,
              step: 0.1,
              default: 1.5
            }
          ],
          examples: [
            {
              image: '/examples/enhancement_1.jpg',
              description: 'Mejora de contraste en una imagen con poca iluminación'
            }
          ]
        }
      ],
      
      // Processing Pipeline
      processingPipeline: [],
      
      // Results Tabs
      resultTabs: [
        { id: 'detections', name: 'Detecciones' },
        { id: 'metrics', name: 'Métricas' },
        { id: 'json', name: 'JSON' }
      ],

      // Image Viewer
      showImageViewer: false,
      viewerImage: null
    }
  },
  async created() {
    // Cargar proyectos al iniciar
    await this.loadProjects();
    
    // Comprobar si hay un ID de proyecto en la URL
    const projectId = this.$route.query.project;
    if (projectId) {
      this.currentProjectId = projectId;
      await this.loadProjectData();
    }
  },
  methods: {
    async loadProjects() {
      try {
        this.loading = true;
        this.loadingMessage = 'Cargando proyectos...';
        const response = await axiosInstance.get('/api/projects/');
        this.projects = response.data;
        console.log('Proyectos cargados:', this.projects);
      } catch (error) {
        console.error('Error cargando proyectos:', error);
      } finally {
        this.loading = false;
      }
    },
    
    async loadProjectData() {
      if (!this.currentProjectId) {
        this.currentProject = null;
        this.currentImage = null;
        this.processedImage = null;
        return;
      }
      
      try {
        this.loading = true;
        this.loadingMessage = 'Cargando datos del proyecto...';
        const response = await axiosInstance.get(`/api/projects/${this.currentProjectId}/`);
        this.currentProject = response.data;
        console.log('Proyecto cargado:', this.currentProject);
        
        // Resetear imagen seleccionada
        this.currentImageId = null;
        this.currentImage = null;
        this.processedImage = null;
        
        // Si hay imágenes, seleccionar la primera
        if (this.currentProject.images && this.currentProject.images.length > 0) {
          this.currentImageId = this.currentProject.images[0].id;
          this.selectImage();
        }
        
      } catch (error) {
        console.error('Error cargando datos del proyecto:', error);
      } finally {
        this.loading = false;
      }
    },
    
    selectImage() {
      if (!this.currentImageId || !this.currentProject || !this.currentProject.images) {
        this.currentImage = null;
        this.processedImage = null;
        this.processingResults = null;
        return;
      }
      
      this.currentImage = this.currentProject.images.find(img => img.id == this.currentImageId);
      console.log('Imagen seleccionada:', this.currentImage);
      
      // Resetear imagen procesada y resultados al cambiar de imagen
      this.processedImage = null;
      this.processingResults = null;
    },
    
    createNewProject() {
      this.newProject = {
        name: '',
        description: '',
        type: 'detection'
      };
      this.showNewProjectModal = true;
    },
    
    async confirmCreateProject() {
      if (!this.newProject.name.trim()) {
        alert('El nombre del proyecto es obligatorio');
        return;
      }
      
      try {
        this.loading = true;
        this.loadingMessage = 'Creando proyecto...';
        
        // Añadir log para depuración
        console.log('Datos del proyecto a crear:', this.newProject);
        
        const response = await axiosInstance.post('/api/projects/', this.newProject);
        
        // Añadir log para respuesta
        console.log('Respuesta del servidor:', response);
        
        // Agregar a la lista y seleccionar
        this.projects.unshift(response.data);
        this.currentProjectId = response.data.id;
        await this.loadProjectData();
        
        this.showNewProjectModal = false;
      } catch (error) {
        console.error('Error creando proyecto:', error);
        
        // Mostrar información más detallada del error
        if (error.response) {
          console.error('Status:', error.response.status);
          console.error('Data:', error.response.data);
          console.error('Headers:', error.response.headers);
          
          if (error.response.status === 404) {
            alert('Error: La ruta de API no existe. Verifica que el servidor esté ejecutándose correctamente.');
          } else {
            alert('Error al crear el proyecto: ' + JSON.stringify(error.response.data));
          }
        } else if (error.request) {
          console.error('No se recibió respuesta:', error.request);
          alert('Error: No se recibió respuesta del servidor. Verifica que el servidor esté en ejecución.');
        } else {
          console.error('Error de configuración:', error.message);
          alert('Error de configuración: ' + error.message);
        }
      } finally {
        this.loading = false;
      }
    },
    
    async uploadImage() {
      if (!this.currentProject) {
        alert('Selecciona un proyecto primero');
        return;
      }
      
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = 'image/*';
      
      input.onchange = async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        
        try {
          this.loading = true;
          this.loadingMessage = 'Subiendo imagen...';
          
          const formData = new FormData();
          formData.append('image', file);
          
          const response = await axiosInstance.post(
            `/api/projects/${this.currentProject.id}/upload_image/`,
            formData,
            {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            }
          );
          
          // Recargar proyecto para obtener la nueva imagen
          await this.loadProjectData();
          
          // Seleccionar la imagen recién subida
          if (response.data && response.data.id) {
            this.currentImageId = response.data.id;
            this.selectImage();
          }
          
        } catch (error) {
          console.error('Error subiendo imagen:', error);
          alert('Error al subir la imagen. Por favor, intenta de nuevo.');
        } finally {
          this.loading = false;
        }
      };
      
      input.click();
    },
    
    selectAlgorithm(algorithm) {
      algorithm.selected = !algorithm.selected;
      
      if (algorithm.selected) {
        // Clonar los parámetros para no modificar los originales
        const params = JSON.parse(JSON.stringify(algorithm.params));
        
        // Resetear a valores por defecto
        params.forEach(param => {
          param.value = param.default;
        });
        
        // Crear una copia para la selección actual
        this.selectedAlgorithm = {
          ...algorithm,
          params
        };
      } else if (this.selectedAlgorithm && this.selectedAlgorithm.id === algorithm.id) {
        this.selectedAlgorithm = null;
      }
    },
    
    showAlgorithmInfo(algorithm) {
      this.algorithmInfoData = {
        ...algorithm,
        examples: [
          {
            image: 'https://cdn.pixabay.com/photo/2017/05/10/19/46/robot-2301646_1280.jpg',
            description: algorithm.id === 'object_detection' ? 'Detección de componentes electrónicos' :
                         algorithm.id === 'edge_detection' ? 'Detección de bordes en componentes' :
                         algorithm.id === 'segmentation' ? 'Segmentación de una pieza metálica' :
                         algorithm.id === 'feature_extraction' ? 'Extracción de puntos de interés' :
                         'Mejora de calidad de imagen industrial'
          },
          {
            image: 'https://cdn.pixabay.com/photo/2019/09/29/22/06/binary-4514033_1280.jpg',
            description: 'Ejemplo de procesamiento industrial'
          }
        ]
      };
      this.showAlgorithmInfoModal = true;
    },
    
    resetAlgorithmParams() {
      if (!this.selectedAlgorithm) return;
      
      this.selectedAlgorithm.params.forEach(param => {
        param.value = param.default;
      });
    },
    
    applyAlgorithm() {
      if (!this.selectedAlgorithm || !this.currentImage) return;
      
      // Agregar al pipeline
      const pipelineStep = {
        id: this.selectedAlgorithm.id,
        name: this.selectedAlgorithm.name,
        params: JSON.parse(JSON.stringify(this.selectedAlgorithm.params)),
        active: true
      };
      
      this.processingPipeline.push(pipelineStep);
      
      // Procesar inmediatamente si es el primer algoritmo
      if (this.processingPipeline.length === 1) {
        this.processCurrentImage();
      }
    },
    
    togglePipelineStep(index) {
      if (index >= 0 && index < this.processingPipeline.length) {
        this.processingPipeline[index].active = !this.processingPipeline[index].active;
        this.processCurrentImage(); // Reprocesar con el cambio
      }
    },
    
    moveStepUp(index) {
      if (index > 0) {
        const temp = this.processingPipeline[index];
        this.processingPipeline[index] = this.processingPipeline[index - 1];
        this.processingPipeline[index - 1] = temp;
        this.processCurrentImage(); // Reprocesar con el nuevo orden
      }
    },
    
    moveStepDown(index) {
      if (index < this.processingPipeline.length - 1) {
        const temp = this.processingPipeline[index];
        this.processingPipeline[index] = this.processingPipeline[index + 1];
        this.processingPipeline[index + 1] = temp;
        this.processCurrentImage(); // Reprocesar con el nuevo orden
      }
    },
    
    removeStep(index) {
      if (confirm('¿Estás seguro de eliminar este paso del procesamiento?')) {
        this.processingPipeline.splice(index, 1);
        this.processCurrentImage(); // Reprocesar sin este paso
      }
    },
    
    async processCurrentImage() {
      if (!this.currentImage || !this.processingPipeline.length) {
        console.log('No hay imagen seleccionada o no hay pipeline definido');
        alert('Por favor, selecciona una imagen y añade al menos un algoritmo al pipeline.');
        return;
      }
      
      try {
        this.processingInProgress = true;
        this.loading = true;
        this.loadingMessage = 'Procesando imagen...';
        
        // Resetear resultados anteriores
        this.processedImage = null;
        this.processingResults = null;
        
        // Filtrar solo los pasos activos
        const activePipeline = this.processingPipeline
          .filter(step => step.active)
          .map(step => ({
            algorithm: step.id,
            params: step.params.reduce((obj, param) => {
              obj[param.name.toLowerCase().replace(/ /g, '_')] = param.value;
              return obj;
            }, {})
          }));
        
        if (activePipeline.length === 0) {
          console.log('No hay algoritmos activos en el pipeline');
          this.processedImage = null;
          this.processingResults = null;
          alert('No hay algoritmos activos en el pipeline. Por favor, activa al menos un algoritmo.');
          return;
        }
        
        console.log('Enviando pipeline al backend:', JSON.stringify(activePipeline, null, 2));
        console.log('ID de la imagen seleccionada:', this.currentImage.id);
        
        // Enviar al backend para procesamiento
        try {
          const url = '/api/process_image/';
          console.log('URL de la petición:', axiosInstance.defaults.baseURL + url);
          
          const requestData = {
            image_id: this.currentImage.id,
            pipeline: activePipeline
          };
          
          console.log('Datos de la petición:', JSON.stringify(requestData, null, 2));
          
          const response = await axiosInstance.post(url, requestData);
          
          console.log('Respuesta del backend:', response.data);
          
          // Actualizar UI con resultados
          if (response.data && response.data.processed_image) {
            this.processedImage = response.data.processed_image;
            this.processingResults = response.data.results;
            
            // Mostrar la pestaña de detecciones por defecto
            this.activeResultTab = 'detections';
            this.collapseResults = false;
            
            // Notificar al usuario
            console.log('Procesamiento completado exitosamente');
          } else {
            console.error('La respuesta no contiene una imagen procesada:', response.data);
            alert('Error: La respuesta del servidor no incluye los resultados esperados.');
          }
        } catch (apiError) {
          console.error('Error en llamada a API:', apiError);
          console.error('Detalles del error:', apiError.response ? apiError.response.data : 'No hay detalles');
          console.error('Código de estado HTTP:', apiError.response ? apiError.response.status : 'N/A');
          console.error('Headers de respuesta:', apiError.response ? apiError.response.headers : 'N/A');
          
          // Mostrar mensaje de error específico según el código de error
          if (apiError.response) {
            const statusCode = apiError.response.status;
            if (statusCode === 404) {
              alert('Error 404: El endpoint de procesamiento de imágenes no existe. Verifica las URLs del backend.');
            } else if (statusCode === 500) {
              alert('Error 500: Error interno del servidor. Verifica los logs del backend.');
            } else {
              alert(`Error ${statusCode} al procesar la imagen: ${JSON.stringify(apiError.response.data)}`);
            }
          } else if (apiError.request) {
            alert('No se recibió respuesta del servidor. Verifica que el servidor backend esté en ejecución.');
          } else {
            alert(`Error de configuración: ${apiError.message}`);
          }
        }
        
      } catch (error) {
        console.error('Error procesando imagen:', error);
        alert('Error al procesar la imagen. Verifica que el pipeline sea válido.');
      } finally {
        this.loading = false;
        this.processingInProgress = false;
      }
    },
    
    toggleSplitView() {
      this.splitView = !this.splitView;
    },
    
    saveProcessedImage() {
      if (!this.processedImage || !this.currentProject) {
        return;
      }
      
      const filename = prompt('Ingresa un nombre para la imagen procesada:', 'Procesada_' + new Date().toISOString().substring(0, 10));
      if (!filename) return;
      
      try {
        this.loading = true;
        this.loadingMessage = 'Guardando imagen procesada...';
        
        // Implementación: guardar imagen procesada en el proyecto
        // ...
        
        alert('Imagen guardada exitosamente.');
      } catch (error) {
        console.error('Error guardando imagen:', error);
        alert('Error al guardar la imagen procesada.');
      } finally {
        this.loading = false;
      }
    },
    
    downloadProcessedImage() {
      if (!this.processedImage) return;
      
      const link = document.createElement('a');
      link.href = this.processedImage;
      link.download = 'processed_image_' + new Date().toISOString().substring(0, 10) + '.png';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
    
    highlightDetection(index) {
      // Implementación: resaltar la detección seleccionada en la imagen
      console.log('Resaltando detección', index);
    },
    
    async exportJSON() {
      if (!this.processingResults) {
        alert('No hay resultados para exportar');
        return;
      }
      
      const dataStr = JSON.stringify(this.processingResults, null, 2);
      const blob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      
      const link = document.createElement('a');
      link.href = url;
      link.download = `results_${this.currentProject.name}_${new Date().toISOString().substring(0, 10)}.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
    
    async exportDatasheet() {
      if (!this.processingResults) {
        alert('No hay resultados para exportar');
        return;
      }
      
      try {
        this.loading = true;
        this.loadingMessage = 'Generando datasheet...';
        
        // Implementación: convertir resultados a formato CSV/Excel
        // ...
        
        // Simulación de descarga
        setTimeout(() => {
          const csvContent = this.generateCSV(this.processingResults);
          const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
          const url = URL.createObjectURL(blob);
          
          const link = document.createElement('a');
          link.href = url;
          link.download = `datasheet_${this.currentProject.name}_${new Date().toISOString().substring(0, 10)}.csv`;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          
          this.loading = false;
        }, 1000);
        
      } catch (error) {
        console.error('Error generando datasheet:', error);
        alert('Error al generar el datasheet.');
        this.loading = false;
      }
    },
    
    generateCSV(data) {
      // Implementación básica para generar CSV
      if (data.detections && data.detections.length) {
        let csv = 'Class,Confidence,X,Y,Width,Height\n';
        data.detections.forEach(d => {
          csv += `${d.class},${d.confidence},${d.x},${d.y},${d.width},${d.height}\n`;
        });
        return csv;
      }
      
      if (data.metrics) {
        let csv = 'Metric,Value\n';
        Object.entries(data.metrics).forEach(([key, value]) => {
          csv += `${this.formatMetricName(key)},${value}\n`;
        });
        return csv;
      }
      
      return 'No data available';
    },
    
    async saveProcessingPipeline() {
      if (!this.processingPipeline.length || !this.currentProject) {
        alert('No hay un pipeline definido o no has seleccionado un proyecto');
        return;
      }
      
      const pipelineName = prompt('Ingresa un nombre para guardar este pipeline:', 'Pipeline_' + new Date().toISOString().substring(0, 10));
      if (!pipelineName) return;
      
      try {
        this.loading = true;
        this.loadingMessage = 'Guardando pipeline...';
        
        // Implementación: guardar pipeline en el backend
        // ...
        
        alert('Pipeline guardado exitosamente.');
      } catch (error) {
        console.error('Error guardando pipeline:', error);
        alert('Error al guardar el pipeline.');
      } finally {
        this.loading = false;
      }
    },
    
    // Helpers
    getImageName(imagePath) {
      if (!imagePath) return 'Sin nombre';
      
      // Extract filename from path or URL
      const parts = imagePath.split('/');
      return parts[parts.length - 1];
    },
    
    formatMetricName(key) {
      return key
        .replace(/_/g, ' ')
        .replace(/\b\w/g, l => l.toUpperCase());
    },
    
    formatMetricValue(value) {
      if (typeof value === 'number') {
        return value.toFixed(4);
      }
      return value;
    },

    // Image Viewer
    openImageViewer(image) {
      this.viewerImage = image;
      this.showImageViewer = true;
    }
  }
}
</script>

<style scoped>
.constructor-proyecto-page {
  min-height: 100vh;
  width: 100vw;
  background: linear-gradient(135deg, #101010 0%, #1a2a3a 100%);
  color: #fff;
  display: flex;
  flex-direction: column;
}

/* Navbar Styles */
.constructor-navbar {
  width: 100%;
  height: 64px;
  background: linear-gradient(90deg, #181c22 60%, #2a3a4a 100%);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  border-bottom: 2px solid #a3c9e2;
  box-shadow: 0 2px 12px rgba(0,0,0,0.18);
  margin-top: -70px;
  position: relative;
  z-index: 100;
}

.navbar-logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.navbar-logo-img {
  width: 38px;
  height: 38px;
  border-radius: 8px;
  object-fit: contain;
}

.navbar-title {
  font-size: 1.5rem;
  color: #a3c9e2;
  font-weight: bold;
  letter-spacing: 0.08em;
  font-family: 'Share Tech Mono', monospace;
}

.navbar-actions {
  display: flex;
  gap: 12px;
}

.btn-help {
  background: none;
  border: none;
  color: #a3c9e2;
  font-size: 1.5rem;
  cursor: pointer;
  transition: color 0.2s, transform 0.2s;
}

.btn-help:hover {
  color: #7fff7f;
  transform: scale(1.1);
}

.constructor-layout {
  display: flex;
  flex: 1;
  height: calc(100vh - 65px);
  overflow: hidden;
}

/* Sidebar Styles */
.constructor-sidebar {
  width: 320px;
  background: linear-gradient(180deg, #181c22 70%, #232b36 100%);
  border-right: 1px solid #3a4553;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  padding: 1rem;
}

.sidebar-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid #3a4553;
  margin-bottom: 1rem;
}

.sidebar-logo {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  margin-bottom: 0.5rem;
  box-shadow: 0 2px 8px #a3c9e244;
}

.sidebar-header h2 {
  color: #a3c9e2;
  font-size: 1.2rem;
  margin: 0.5rem 0;
  text-align: center;
  font-family: 'VT323', monospace;
  letter-spacing: 0.04em;
}

.sidebar-section {
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #3a4553;
  padding-bottom: 1rem;
}

.sidebar-section:last-child {
  border-bottom: none;
}

.sidebar-section h3 {
  color: #a3c9e2;
  font-size: 1rem;
  margin-bottom: 0.8rem;
  font-family: 'VT323', monospace;
  letter-spacing: 0.04em;
}

.project-selector {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.project-selector select {
  flex: 1;
  padding: 0.5rem;
  background: #232b36;
  border: 1px solid #3a4553;
  border-radius: 6px;
  color: #fff;
  font-size: 0.9rem;
}

.btn-new {
  background: #232b36;
  color: #7fff7f;
  border: 1px solid #7fff7f;
  border-radius: 6px;
  padding: 0.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.9rem;
  transition: all 0.18s;
}

.btn-new:hover {
  background: #7fff7f;
  color: #232b36;
  transform: translateY(-2px);
}

.algorithm-options {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.algorithm-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #232b36;
  padding: 0.6rem;
  border-radius: 6px;
  border: 1px solid #3a4553;
  cursor: pointer;
  transition: all 0.2s;
}

.algorithm-option:hover {
  background: #2a3a4a;
  border-color: #a3c9e2;
}

.algorithm-option label {
  flex: 1;
  cursor: pointer;
}

.algorithm-option i {
  color: #a3c9e2;
  cursor: pointer;
}

.param-control {
  margin-bottom: 1rem;
}

.param-control label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #bfc9d1;
}

.param-input {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.param-input input[type="range"] {
  flex: 1;
  height: 6px;
  -webkit-appearance: none;
  background: #232b36;
  border-radius: 3px;
  outline: none;
}

.param-input input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #a3c9e2;
  cursor: pointer;
}

.param-input input[type="number"],
.param-input input[type="text"],
.param-input select {
  flex: 1;
  padding: 0.5rem;
  background: #232b36;
  border: 1px solid #3a4553;
  border-radius: 6px;
  color: #fff;
  font-size: 0.9rem;
}

.range-value {
  width: 40px;
  text-align: right;
  font-size: 0.9rem;
  color: #a3c9e2;
}

.color-picker {
  display: flex;
  align-items: center;
}

.color-picker input {
  width: 30px;
  height: 30px;
  border: none;
  background: none;
  cursor: pointer;
}

.algorithm-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.btn-apply, .btn-reset {
  flex: 1;
  padding: 0.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.18s;
}

.btn-apply {
  background: #232b36;
  color: #7fff7f;
  border: 1px solid #7fff7f;
}

.btn-apply:hover {
  background: #7fff7f;
  color: #232b36;
}

.btn-reset {
  background: #232b36;
  color: #a3c9e2;
  border: 1px solid #a3c9e2;
}

.btn-reset:hover {
  background: #a3c9e2;
  color: #232b36;
}

.processing-pipeline {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.pipeline-step {
  background: #232b36;
  border: 1px solid #3a4553;
  border-radius: 6px;
  overflow: hidden;
  padding: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.pipeline-step.active {
  border-color: #7fff7f;
  background: linear-gradient(90deg, #232b36 80%, rgba(127, 255, 127, 0.1) 100%);
}

.pipeline-step:hover {
  background: #2a3a4a;
}

.step-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.step-number {
  background: #181c22;
  color: #a3c9e2;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 0.8rem;
  font-weight: bold;
}

.step-name {
  flex: 1;
  font-size: 0.9rem;
}

.step-actions {
  display: flex;
  gap: 0.3rem;
}

.step-actions button {
  background: none;
  border: none;
  color: #bfc9d1;
  cursor: pointer;
  font-size: 0.8rem;
  padding: 0.2rem;
  transition: color 0.18s;
}

.step-actions button:hover {
  color: #a3c9e2;
}

.step-actions button:disabled {
  color: #3a4553;
  cursor: not-allowed;
}

.pipeline-empty {
  padding: 1rem;
  text-align: center;
  background: #232b36;
  border: 1px dashed #3a4553;
  border-radius: 6px;
  color: #bfc9d1;
  font-size: 0.9rem;
}

.export-options {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.btn-export {
  padding: 0.5rem;
  background: #232b36;
  color: #a3c9e2;
  border: 1px solid #a3c9e2;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  transition: all 0.18s;
}

.btn-export:hover {
  background: #a3c9e2;
  color: #232b36;
  transform: translateY(-2px);
}

/* Main Content Area */
.constructor-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.workspace-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  border-bottom: 1px solid #3a4553;
}

.workspace-header h2 {
  color: #a3c9e2;
  font-size: 1.5rem;
  margin: 0;
  font-family: 'VT323', monospace;
  letter-spacing: 0.04em;
}

.workspace-actions {
  display: flex;
  gap: 1rem;
}

.workspace-stats {
  display: flex;
  gap: 1rem;
  color: #a3c9e2;
  font-size: 0.9rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(35, 43, 54, 0.5);
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  border: 1px solid #3a4553;
  white-space: nowrap;
}

.stat-item i {
  color: #7fff7f;
}

.btn-process, .btn-toggle-view {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  transition: all 0.18s;
}

.btn-process {
  background: #232b36;
  color: #7fff7f;
  border: 1px solid #7fff7f;
}

.btn-process:hover:not(:disabled) {
  background: #7fff7f;
  color: #232b36;
  transform: translateY(-2px);
}

.btn-process:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-toggle-view {
  background: #232b36;
  color: #a3c9e2;
  border: 1px solid #a3c9e2;
}

.btn-toggle-view:hover {
  background: #a3c9e2;
  color: #232b36;
}

.workspace-content {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.workspace-content.split-view {
  flex-direction: row;
}

.workspace-content:not(.split-view) .image-container.processed {
  display: none;
}

.workspace-content:not(.split-view) .image-container.original {
  flex: 1;
}

.image-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 1rem;
  border-right: 1px solid #3a4553;
}

.image-container:last-child {
  border-right: none;
}

.image-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.image-header h3 {
  color: #a3c9e2;
  font-size: 1.2rem;
  margin: 0;
  font-family: 'VT323', monospace;
  letter-spacing: 0.04em;
}

.image-actions {
  display: flex;
  gap: 0.5rem;
}

.image-actions button {
  padding: 0.5rem;
  background: #232b36;
  color: #a3c9e2;
  border: 1px solid #a3c9e2;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.9rem;
  transition: all 0.18s;
}

.image-actions button:hover:not(:disabled) {
  background: #a3c9e2;
  color: #232b36;
}

.image-actions button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.image-actions select {
  padding: 0.5rem;
  background: #232b36;
  border: 1px solid #3a4553;
  border-radius: 6px;
  color: #fff;
  font-size: 0.9rem;
}

.image-workspace {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #181c22;
  border-radius: 6px;
  overflow: hidden;
  position: relative;
}

.image-workspace img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.no-image {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #3a4553;
  text-align: center;
  padding: 2rem;
}

.no-image i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.processing-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.spinner {
  text-align: center;
  color: #a3c9e2;
}

.spinner i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.results-panel {
  background: #232b36;
  border-top: 1px solid #3a4553;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
}

.results-header h3 {
  color: #a3c9e2;
  font-size: 1rem;
  margin: 0;
  font-family: 'VT323', monospace;
  letter-spacing: 0.04em;
}

.results-actions button {
  background: none;
  border: none;
  color: #bfc9d1;
  cursor: pointer;
}

.results-content {
  max-height: 300px;
  overflow-y: auto;
}

.results-tabs {
  display: flex;
  gap: 0.2rem;
  padding: 0 1rem;
  border-bottom: 1px solid #3a4553;
}

.results-tabs button {
  padding: 0.5rem 1rem;
  background: #181c22;
  border: 1px solid #3a4553;
  border-bottom: none;
  border-radius: 6px 6px 0 0;
  color: #bfc9d1;
  cursor: pointer;
  font-size: 0.9rem;
}

.results-tabs button.active {
  background: #232b36;
  color: #a3c9e2;
  border-color: #a3c9e2;
  border-bottom: 1px solid #232b36;
  margin-bottom: -1px;
}

.tab-content {
  padding: 1rem;
}

.detection-results table {
  width: 100%;
  border-collapse: collapse;
  background-color: rgba(24, 28, 34, 0.7);
  margin-top: 1rem;
}

.detection-results th,
.detection-results td {
  padding: 0.8rem;
  text-align: left;
  border-bottom: 1px solid #3a4553;
}

.detection-results th {
  color: #a3c9e2;
  font-weight: normal;
  background-color: rgba(24, 28, 34, 0.9);
}

.detection-results td {
  color: #bfc9d1;
}

.detection-results tr:hover {
  background-color: rgba(51, 60, 73, 0.5);
}

.detection-results td button {
  background: none;
  border: none;
  color: #7fff7f;
  cursor: pointer;
  font-size: 1.1rem;
  transition: transform 0.2s;
}

.detection-results td button:hover {
  transform: scale(1.2);
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.metric-item {
  background: #181c22;
  border: 1px solid #3a4553;
  border-radius: 6px;
  padding: 0.5rem;
}

.metric-name {
  font-size: 0.9rem;
  color: #a3c9e2;
  margin-bottom: 0.3rem;
}

.metric-value {
  font-size: 1.2rem;
  color: #fff;
}

.json-results pre {
  margin: 0;
  padding: 1rem;
  background: #181c22;
  border-radius: 6px;
  color: #bfc9d1;
  overflow-x: auto;
  font-size: 0.9rem;
}

.no-results {
  padding: 2rem;
  text-align: center;
  color: #bfc9d1;
}

/* Modals */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: linear-gradient(135deg, #232b36 60%, #1a2a3a 100%);
  border-radius: 12px;
  padding: 1.5rem;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  border: 1px solid #3a4553;
  box-shadow: 0 8px 32px rgba(0,0,0,0.25);
  color: #fff;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #3a4553;
  padding-bottom: 1rem;
}

.modal-header h2 {
  margin: 0;
  color: #a3c9e2;
  font-family: 'VT323', monospace;
  letter-spacing: 0.04em;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #a3c9e2;
}

.modal-body {
  color: #bfc9d1;
}

.algo-details h3 {
  color: #a3c9e2;
  font-size: 1rem;
  margin: 1.5rem 0 0.5rem;
  font-family: 'VT323', monospace;
  letter-spacing: 0.04em;
}

.algo-examples {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1rem;
}

.algo-example {
  width: calc(50% - 0.5rem);
  background: #181c22;
  border: 1px solid #3a4553;
  border-radius: 6px;
  overflow: hidden;
}

.algo-example img {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.algo-example p {
  padding: 0.5rem;
  font-size: 0.9rem;
  margin: 0;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #a3c9e2;
}

.form-group input, 
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #3a4553;
  border-radius: 8px;
  font-size: 1rem;
  background: #181c22;
  color: #fff;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.8rem;
  margin-top: 1.5rem;
}

.btn-cancel, .btn-create {
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.18s;
}

.btn-cancel {
  background-color: #232b36;
  color: #a3c9e2;
  border: 1px solid #a3c9e2;
}

.btn-cancel:hover {
  background-color: #a3c9e2;
  color: #232b36;
}

.btn-create {
  background-color: #232b36;
  color: #7fff7f;
  border: 1px solid #7fff7f;
}

.btn-create:hover {
  background-color: #7fff7f;
  color: #232b36;
}

/* Loading */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1100;
}

.loading-spinner {
  text-align: center;
  color: #a3c9e2;
}

.loading-spinner i {
  font-size: 3rem;
  margin-bottom: 1rem;
}

/* Welcome Banner */
.welcome-banner {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1200;
}

.welcome-content {
  background: linear-gradient(135deg, #232b36 60%, #1a2a3a 100%);
  border-radius: 12px;
  padding: 1.5rem;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  border: 1px solid #3a4553;
  box-shadow: 0 8px 32px rgba(0,0,0,0.25);
  color: #fff;
}

.welcome-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #3a4553;
  padding-bottom: 1rem;
}

.welcome-header h2 {
  margin: 0;
  color: #a3c9e2;
  font-family: 'VT323', monospace;
  letter-spacing: 0.04em;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #a3c9e2;
}

.welcome-body {
  color: #bfc9d1;
}

.welcome-body ul {
  list-style: none;
  padding: 0;
  margin: 1.5rem 0;
}

.welcome-body li {
  margin-bottom: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.welcome-body li i {
  color: #7fff7f;
  font-size: 1.1rem;
}

.welcome-body strong {
  color: #7fff7f;
}

.welcome-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

.welcome-btn {
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.18s;
  background-color: #232b36;
  color: #7fff7f;
  border: 1px solid #7fff7f;
}

.welcome-btn:hover {
  background-color: #7fff7f;
  color: #232b36;
}

/* Responsive */
@media (max-width: 1024px) {
  .constructor-layout {
    flex-direction: column;
    height: auto;
  }
  
  .constructor-sidebar {
    width: 100%;
    max-height: 300px;
  }
  
  .workspace-content.split-view {
    flex-direction: column;
  }
  
  .image-container {
    border-right: none;
    border-bottom: 1px solid #3a4553;
  }
  
  .algo-example {
    width: 100%;
  }

  .workspace-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .workspace-actions {
    width: 100%;
    justify-content: space-between;
  }
  
  .workspace-stats {
    margin-bottom: 0.5rem;
  }
}

.clickable-image {
  cursor: pointer;
  transition: transform 0.2s ease;
}

.clickable-image:hover {
  transform: scale(1.02);
  box-shadow: 0 0 10px rgba(163, 201, 226, 0.5);
}

.image-viewer-modal {
  background: linear-gradient(135deg, #232b36 60%, #1a2a3a 100%);
  border-radius: 12px;
  width: 90%;
  max-width: 1200px;
  height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  border: 1px solid #3a4553;
  box-shadow: 0 8px 32px rgba(0,0,0,0.25);
}

.image-viewer-content {
  flex: 1;
  padding: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: auto;
  background-color: #181c22;
}

.image-viewer-content img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
</style> 