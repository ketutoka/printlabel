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
        const response = await fetch(`http://localhost:8002/labels/preview/${labelId}?token=${encodeURIComponent(token)}`)
        
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
    }
  }
})