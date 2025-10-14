import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle common errors
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Helper function to get image URL with authorization
export const getImageUrl = (path) => {
  const token = localStorage.getItem('token')
  const baseUrl = 'http://localhost:8000'
  if (token) {
    return `${baseUrl}${path}?Authorization=Bearer ${encodeURIComponent(token)}`
  }
  return `${baseUrl}${path}`
}

export default api