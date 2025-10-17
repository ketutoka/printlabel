import { defineStore } from 'pinia'
import api, { getImageUrl } from '../services/api'

export const useLabelStore = defineStore('label', {
  state: () => ({
    labels: [],
    currentLabel: null,
    loading: false,
    error: null
  }),

  actions: {
    async createLabel(labelData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.post('/labels/generate', labelData)
        this.currentLabel = response.data
        this.labels.unshift(response.data) // Add to beginning of array
        return { success: true, data: response.data }
      } catch (error) {
        this.error = error.response?.data?.detail || 'Gagal membuat label'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async getLabelForPrint(labelId) {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.get(`/labels/print/${labelId}`)
        return { success: true, data: response.data }
      } catch (error) {
        this.error = error.response?.data?.detail || 'Gagal mengambil data label'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async getPreviewUrl(labelId) {
      try {
        const token = localStorage.getItem('token')
        const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8002'
        
        // Handle relative URLs for production
        const fullUrl = baseUrl.startsWith('/') ? `${window.location.origin}${baseUrl}` : baseUrl
        
        const response = await fetch(`${fullUrl}/labels/preview/${labelId}?token=${encodeURIComponent(token)}`)
        
        if (!response.ok) {
          throw new Error('Failed to fetch image')
        }
        
        const blob = await response.blob()
        return URL.createObjectURL(blob)
      } catch (error) {
        console.error('Error fetching preview:', error)
        throw error
      }
    },

    async fetchLabels() {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.get('/labels')
        this.labels = response.data || []
        return { success: true, data: response.data }
      } catch (error) {
        this.error = error.response?.data?.detail || 'Gagal memuat daftar label'
        console.error('Error fetching labels:', error)
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    clearError() {
      this.error = null
    },

    clearLabels() {
      this.labels = []
      this.currentLabel = null
      this.error = null
    },

    setCurrentLabel(label) {
      this.currentLabel = label
    },

    async deleteLabel(labelId) {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.delete(`/labels/${labelId}`)
        
        // Remove from local state
        this.labels = this.labels.filter(label => label.id !== labelId)
        
        // Clear current label if it was deleted
        if (this.currentLabel && this.currentLabel.id === labelId) {
          this.currentLabel = null
        }
        
        return { success: true, message: response.data.message }
      } catch (error) {
        this.error = error.response?.data?.detail || 'Gagal menghapus label'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async bulkDeleteLabels(labelIds) {
      this.loading = true
      this.error = null
      
      try {
        const response = await api.delete('/labels/bulk', { data: labelIds })
        
        // Remove deleted labels from local state
        this.labels = this.labels.filter(label => !labelIds.includes(label.id))
        
        // Clear current label if it was among deleted ones
        if (this.currentLabel && labelIds.includes(this.currentLabel.id)) {
          this.currentLabel = null
        }
        
        return { 
          success: true, 
          message: response.data.message,
          results: response.data
        }
      } catch (error) {
        this.error = error.response?.data?.detail || 'Gagal menghapus label'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    }
  }
})