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
        
        // Load user's shipping labels after successful login
        const { useShippingStore } = await import('./shipping')
        const shippingStore = useShippingStore()
        await shippingStore.fetchShippingLabels()
        
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
      
      // Clear shipping labels when logout
      try {
        const { useShippingStore } = require('./shipping')
        const shippingStore = useShippingStore()
        shippingStore.shippingLabels = []
      } catch (e) {
        // Shipping store might not be loaded yet
      }
      
      // Redirect to login page
      if (typeof window !== 'undefined' && window.location) {
        window.location.href = '/login'
      }
    },

    async updateProfile(profileData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.put('/auth/me', profileData)
        
        // Update user data in store
        this.user = { ...this.user, ...response.data }
        
        return { success: true, data: response.data }
      } catch (error) {
        console.error('Update profile error:', error)
        this.error = error.response?.data?.detail || 'Gagal memperbarui profil'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    clearError() {
      this.error = null
    }
  }
})