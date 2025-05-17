import { createStore } from 'vuex'

export default createStore({
  state: {
    // Estado de la cámara
    camera: {
      isActive: false,
      stream: null,
      error: null
    },
    
    // Estado de los modelos 3D
    models: {
      currentModel: null,
      modelsList: [],
      isLoading: false,
      error: null
    },
    
    // Estado de la detección de objetos
    detection: {
      isProcessing: false,
      detectedObjects: [],
      currentObject: null,
      error: null
    },
    
    // Configuraciones de la aplicación
    settings: {
      cameraQuality: 'high',
      modelQuality: 'medium',
      autoSave: true,
      notifications: true
    }
  },
  
  mutations: {
    // Mutaciones para la cámara
    SET_CAMERA_STREAM(state, stream) {
      state.camera.stream = stream
      state.camera.isActive = true
    },
    STOP_CAMERA(state) {
      if (state.camera.stream) {
        state.camera.stream.getTracks().forEach(track => track.stop())
      }
      state.camera.stream = null
      state.camera.isActive = false
    },
    SET_CAMERA_ERROR(state, error) {
      state.camera.error = error
    },
    
    // Mutaciones para los modelos 3D
    SET_CURRENT_MODEL(state, model) {
      state.models.currentModel = model
    },
    ADD_MODEL(state, model) {
      state.models.modelsList.push(model)
    },
    SET_MODELS_LOADING(state, isLoading) {
      state.models.isLoading = isLoading
    },
    SET_MODELS_ERROR(state, error) {
      state.models.error = error
    },
    
    // Mutaciones para la detección de objetos
    SET_DETECTION_PROCESSING(state, isProcessing) {
      state.detection.isProcessing = isProcessing
    },
    SET_DETECTED_OBJECTS(state, objects) {
      state.detection.detectedObjects = objects
    },
    SET_CURRENT_OBJECT(state, object) {
      state.detection.currentObject = object
    },
    SET_DETECTION_ERROR(state, error) {
      state.detection.error = error
    },
    
    // Mutaciones para configuraciones
    UPDATE_SETTINGS(state, settings) {
      state.settings = { ...state.settings, ...settings }
    }
  },
  
  actions: {
    // Acciones para la cámara
    async startCamera({ commit }) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
          video: { 
            width: { ideal: 1920 },
            height: { ideal: 1080 }
          } 
        })
        commit('SET_CAMERA_STREAM', stream)
      } catch (error) {
        commit('SET_CAMERA_ERROR', error.message)
      }
    },
    
    stopCamera({ commit }) {
      commit('STOP_CAMERA')
    },
    
    // Acciones para modelos 3D
    async processImage({ commit }, imageData) {
      commit('SET_MODELS_LOADING', true)
      try {
        // Aquí irá la lógica para procesar la imagen y generar el modelo 3D
        // Por ahora es un placeholder
        const model = {
          id: Date.now(),
          name: 'Nuevo Modelo',
          date: new Date(),
          status: 'completed'
        }
        commit('ADD_MODEL', model)
        commit('SET_CURRENT_MODEL', model)
      } catch (error) {
        commit('SET_MODELS_ERROR', error.message)
      } finally {
        commit('SET_MODELS_LOADING', false)
      }
    },
    
    // Acciones para detección de objetos
    async detectObjects({ commit }, imageData) {
      commit('SET_DETECTION_PROCESSING', true)
      try {
        // Aquí irá la lógica para detectar objetos
        // Por ahora es un placeholder
        const objects = [
          { id: 1, name: 'Objeto 1', confidence: 0.95 },
          { id: 2, name: 'Objeto 2', confidence: 0.87 }
        ]
        commit('SET_DETECTED_OBJECTS', objects)
      } catch (error) {
        commit('SET_DETECTION_ERROR', error.message)
      } finally {
        commit('SET_DETECTION_PROCESSING', false)
      }
    },
    
    // Acciones para configuraciones
    updateSettings({ commit }, settings) {
      commit('UPDATE_SETTINGS', settings)
    }
  },
  
  getters: {
    // Getters para la cámara
    isCameraActive: state => state.camera.isActive,
    cameraError: state => state.camera.error,
    
    // Getters para modelos 3D
    currentModel: state => state.models.currentModel,
    modelsList: state => state.models.modelsList,
    isModelsLoading: state => state.models.isLoading,
    modelsError: state => state.models.error,
    
    // Getters para detección de objetos
    isDetectionProcessing: state => state.detection.isProcessing,
    detectedObjects: state => state.detection.detectedObjects,
    currentObject: state => state.detection.currentObject,
    detectionError: state => state.detection.error,
    
    // Getters para configuraciones
    settings: state => state.settings
  }
}) 