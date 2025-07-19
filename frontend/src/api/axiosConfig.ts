import axios from 'axios'

/**
 * Axios instance configured for JWT authentication.
 * Automatically attaches token from localStorage to requests.
 */
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000',
  withCredentials: true,
})

interface AuthHeaders {
  Authorization?: string
  [key: string]: string | undefined
}

interface RequestConfig {
  headers?: AuthHeaders
  [key: string]: unknown
}

api.interceptors.request.use(
  (config: RequestConfig) => {
    const token = localStorage.getItem('token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error: unknown) => Promise.reject(error)
)

export default api
