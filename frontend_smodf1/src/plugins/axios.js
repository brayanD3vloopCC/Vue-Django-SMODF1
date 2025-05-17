import axios from 'axios'

const api = axios.create({
    baseURL: 'http://localhost:8000/api/usuarios/',
    withCredentials: true, // Importante para las cookies de sesión
    headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    }
})

// Interceptor para manejar errores
api.interceptors.response.use(
    response => response,
    error => {
        if (error.response && error.response.status === 401) {
            // Redirigir al login si la sesión expira
            window.location.href = '/login'
        }
        return Promise.reject(error)
    }
)

export default api 