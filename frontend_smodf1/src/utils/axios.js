import axios from 'axios';

// Definir la URL base del API
const API_URL = 'http://localhost:8000';

// Crear una instancia de axios con la configuración base
const axiosInstance = axios.create({
    baseURL: API_URL,
    withCredentials: false,  // Cambiar a false para evitar problemas de CORS
    headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    },
    maxContentLength: Infinity,
    maxBodyLength: Infinity,
    timeout: 30000 // 30 segundos de timeout
});

// Add request interceptor to handle file uploads
axiosInstance.interceptors.request.use(config => {
    // If we're sending a FormData object (file upload), remove Content-Type header
    // to let the browser set it with the correct boundary
    if (config.data instanceof FormData) {
        delete config.headers['Content-Type'];
    }
    
    // Agregar timestamp para evitar cacheo
    if (config.method === 'get') {
        config.params = config.params || {};
        config.params['_t'] = Date.now();
    }
    
    console.log(`Enviando ${config.method.toUpperCase()} a ${config.url}`, config.data);
    return config;
}, error => {
    console.error('Error en la configuración de la petición:', error);
    return Promise.reject(error);
});

// Interceptor para manejar errores
axiosInstance.interceptors.response.use(
    response => {
        console.log(`Respuesta exitosa de ${response.config.url}:`, response.data);
        return response;
    },
    error => {
        if (error.response) {
            // Handle specific error cases
            console.error(`Error ${error.response.status} en la respuesta:`, error.response.data);
            
            switch (error.response.status) {
                case 413:
                    console.error('Error: Archivo demasiado grande');
                    break;
                case 403:
                    console.error('Error de permisos (403):', error.response.data);
                    break;
                case 500:
                    console.error('Error del servidor:', error.response.data);
                    break;
                case 404:
                    console.error('Recurso no encontrado:', error.config.url);
                    break;
            }
        } else if (error.request) {
            // La petición fue hecha pero no se recibió respuesta
            console.error('No se recibió respuesta del servidor. Verifica si está en ejecución.');
        } else {
            // Error en la configuración de la petición
            console.error('Error al configurar la petición:', error.message);
        }
        return Promise.reject(error);
    }
);

export default axiosInstance; 