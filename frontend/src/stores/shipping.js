import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../services/api'

export const useShippingStore = defineStore('shipping', () => {
  const shippingLabels = ref([])
  const loading = ref(false)
  const error = ref('')

  const generateShippingLabel = async (labelData) => {
    try {
      loading.value = true
      error.value = ''
      
      const response = await api.post('/shipping-labels/generate', labelData)
      
      if (response.data) {
        // Add to beginning of array
        shippingLabels.value.unshift(response.data)
        return { success: true, data: response.data }
      }
    } catch (err) {
      console.error('Generate shipping label error:', err)
      error.value = err.response?.data?.detail || 'Gagal membuat label pengiriman'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const fetchShippingLabels = async () => {
    try {
      loading.value = true
      error.value = ''
      
      const response = await api.get('/shipping-labels')
      
      if (response.data) {
        shippingLabels.value = response.data
        return { success: true, data: response.data }
      }
    } catch (err) {
      console.error('Fetch shipping labels error:', err)
      error.value = err.response?.data?.detail || 'Gagal memuat label pengiriman'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Alias untuk backward compatibility
  const getShippingLabels = fetchShippingLabels

  const getShippingLabelForPrint = async (labelId) => {
    try {
      const response = await api.get(`/shipping-labels/print/${labelId}`)
      
      if (response.data) {
        return { success: true, data: response.data }
      }
    } catch (err) {
      console.error('Get shipping label for print error:', err)
      error.value = err.response?.data?.detail || 'Gagal memuat data label untuk print'
      return { success: false, error: error.value }
    }
  }

  const getPreviewUrl = async (labelId) => {
    try {
      // Get token from localStorage or API service
      const token = localStorage.getItem('token') || api.defaults.headers.common['Authorization']?.replace('Bearer ', '')
      
      if (!token) {
        throw new Error('No authentication token available')
      }
      
      return `${api.defaults.baseURL}/shipping-labels/preview/${labelId}?token=${token}`
    } catch (err) {
      console.error('Get preview URL error:', err)
      error.value = 'Gagal membuat URL preview'
      throw err
    }
  }

  const clearError = () => {
    error.value = ''
  }

  return {
    shippingLabels,
    loading,
    error,
    generateShippingLabel,
    fetchShippingLabels,
    getShippingLabels,
    getShippingLabelForPrint,
    getPreviewUrl,
    clearError
  }
})