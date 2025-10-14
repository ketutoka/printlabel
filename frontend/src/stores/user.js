import { defineStore } from 'pinia'
import api from '../services/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token'),
    loading: false,
    error: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    userName: (state) => state.user?.name || ''
  },

  actions: {
    async login(credentials) {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.post('/auth/login', {
          email: credentials.email,
          password: credentials.password
        })
        const { access_token } = response.data
        
        this.token = access_token
        localStorage.setItem('token', access_token)
        
        // Set token for future requests
        api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
        
        // Get user info
        await this.getCurrentUser()
        
        // Load user's labels after successful login
        const { useLabelStore } = await import('./label')
        const labelStore = useLabelStore()
        await labelStore.fetchLabels()
        
        return { success: true }
      } catch (error) {
        this.error = error.response?.data?.detail || 'Login gagal'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async register(userData) {
      this.loading = true
      this.error = null
      
      try {
        await api.post('/auth/register', userData)
        return { success: true }
      } catch (error) {
        this.error = error.response?.data?.detail || 'Registrasi gagal'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async resetPassword(email) {
      this.loading = true
      this.error = null
      
      try {
        await api.post('/auth/reset-password', null, { params: { email } })
        return { success: true }
      } catch (error) {
        this.error = error.response?.data?.detail || 'Reset password gagal'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async getCurrentUser() {
      if (!this.token) return
      
      try {
        const response = await api.get('/auth/me')
        this.user = response.data
      } catch (error) {
        console.error('Failed to get current user:', error)
        this.logout()
      }
    },

    logout() {
      this.user = null
      this.token = null
      this.error = null
      localStorage.removeItem('token')
      delete api.defaults.headers.common['Authorization']
      
      // Clear labels when logout
      const { useLabelStore } = require('./label')
      const labelStore = useLabelStore()
      labelStore.clearLabels()
    },

    clearError() {
      this.error = null
    }
  }
})