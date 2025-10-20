<template>
  <div class="create-shipping-label-container">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>🏷️ Buat Label Pengiriman</span>
          <small style="color: #909399; font-size: 12px; display: block; margin-top: 5px;">
            Field penerima dan resi bersifat opsional
          </small>
        </div>
      </template>

      <el-form 
        ref="shippingFormRef" 
        :model="shippingForm" 
        :rules="shippingRules"
        :label-width="labelWidth"
        :label-position="labelPosition"
        @submit.prevent="generateShippingLabel"
      >
        <el-divider content-position="left">
          <span style="color: #409eff; font-weight: bold;">📤 PENGIRIM</span>
        </el-divider>

        <el-form-item label="Nama Pengirim" prop="sender_name">
          <el-input 
            v-model="shippingForm.sender_name" 
            placeholder="Nama lengkap pengirim"
            clearable
          />
        </el-form-item>

        <el-form-item label="No HP Pengirim" prop="sender_phone">
          <el-input 
            v-model="shippingForm.sender_phone" 
            placeholder="Contoh: 081234567890"
            clearable
          />
        </el-form-item>

        <el-divider content-position="left">
          <span style="color: #67c23a; font-weight: bold;">📥 PENERIMA (Opsional)</span>
        </el-divider>

        <el-form-item label="Nama Penerima" prop="recipient_name">
          <el-input 
            v-model="shippingForm.recipient_name" 
            placeholder="Nama lengkap penerima (kosongkan jika tidak diperlukan)"
            clearable
          />
        </el-form-item>

        <el-form-item label="Alamat Lengkap" prop="recipient_address">
          <el-input 
            v-model="shippingForm.recipient_address" 
            type="textarea"
            :rows="3"
            placeholder="Alamat lengkap penerima (kosongkan jika tidak diperlukan)"
            clearable
          />
        </el-form-item>

        <el-form-item label="No HP Penerima" prop="recipient_phone">
          <el-input 
            v-model="shippingForm.recipient_phone" 
            placeholder="No HP penerima (kosongkan jika tidak diperlukan)"
            clearable
          />
        </el-form-item>

        <el-divider content-position="left">
          <span style="color: #f56c6c; font-weight: bold;">🏷️ RESI</span>
        </el-divider>

        <el-form-item label="Kode Resi (Opsional)" prop="shipping_code">
          <el-input 
            v-model="shippingForm.shipping_code" 
            placeholder="Scan QR Code/Barcode atau ketik manual"
            clearable
            style="text-transform: uppercase;"
            @input="handleShippingCodeInput"
          >
            <template #append>
              <el-button 
                type="primary" 
                @click="openScanner"
                icon="CameraFilled"
                size="small"
              >
                Scan
              </el-button>
            </template>
          </el-input>
          <div style="font-size: 12px; color: #909399; margin-top: 5px;">
            💡 Tips: Kode resi akan disembunyikan jika dikosongkan
          </div>
        </el-form-item>

        <el-divider content-position="left">
          <span style="color: #e6a23c; font-weight: bold;">📏 UKURAN LABEL</span>
        </el-divider>

        <el-form-item label="Ukuran Printer" prop="label_size">
          <el-radio-group v-model="shippingForm.label_size" class="label-size-group">
            <el-radio-button label="58mm" size="large">
              <div class="radio-content">
                <span class="radio-title">📱 58mm</span>
                <span class="radio-description">Thermal mini (203px)</span>
              </div>
            </el-radio-button>
            <el-radio-button label="80mm" size="large">
              <div class="radio-content">
                <span class="radio-title">🖨️ 80mm</span>
                <span class="radio-description">Thermal standar (284px)</span>
              </div>
            </el-radio-button>
          </el-radio-group>
          <div style="font-size: 12px; color: #909399; margin-top: 8px;">
            💡 Pilih sesuai dengan lebar kertas thermal printer Anda
          </div>
        </el-form-item>

        <el-form-item>
          <div class="shipping-button-group">
            <el-button 
              type="primary" 
              @click="generateShippingLabel"
              :loading="shippingStore.loading"
              size="large"
              class="shipping-action-button shipping-primary-button"
            >
              <span v-if="!shippingStore.loading">🏷️ Buat Label Pengiriman</span>
              <span v-else>⏳ Membuat Label...</span>
            </el-button>
            <el-button 
              @click="resetShippingForm" 
              size="large"
              class="shipping-action-button shipping-secondary-button"
            >
              🔄 Reset Form
            </el-button>
            <el-button 
              type="info" 
              @click="backToDashboard"
              size="large"
              class="shipping-action-button shipping-info-button"
            >
              ⬅️ Kembali
            </el-button>
          </div>          
        </el-form-item>
      </el-form>

      <!-- Error Display -->
      <el-alert
        v-if="shippingStore.error"
        :title="shippingStore.error"
        type="error"
        show-icon
        :closable="false"
        style="margin-top: 20px;"
      />
    </el-card>

    <!-- Preview Dialog -->
    <el-dialog
      v-model="showPreview"
      title="📋 Preview Label Pengiriman"
      :width="dialogWidth"
      :before-close="handleClosePreview"
      :fullscreen="isMobile"
    >
      <div v-if="generatedLabel" class="preview-content">
        <!-- Label Details -->
        <el-row :gutter="20" style="margin-bottom: 20px;">
          <el-col :xs="24" :sm="12" :md="12">
            <el-card shadow="never">
              <template #header>
                <span>📤 Pengirim</span>
              </template>
              <p><strong>Nama:</strong> {{ generatedLabel.sender_name }}</p>
              <p><strong>No HP:</strong> {{ generatedLabel.sender_phone }}</p>
            </el-card>
          </el-col>
          <el-col :xs="24" :sm="12" :md="12">
            <el-card shadow="never">
              <template #header>
                <span>📥 Penerima</span>
              </template>
              <p><strong>Nama:</strong> {{ generatedLabel.recipient_name }}</p>
              <p><strong>Alamat:</strong> {{ generatedLabel.recipient_address }}</p>
              <p><strong>No HP:</strong> {{ generatedLabel.recipient_phone }}</p>
            </el-card>
          </el-col>
        </el-row>

        <el-card shadow="never" style="margin-bottom: 20px;" v-if="generatedLabel.shipping_code">
          <template #header>
            <span>🏷️ Resi Pengiriman</span>
          </template>
          <p style="font-size: 18px; font-weight: bold; color: #409eff;">{{ generatedLabel.shipping_code }}</p>
        </el-card>

        <!-- Preview Image -->
        <div style="text-align: center; margin: 20px 0;">
          <el-button 
            type="info" 
            @click="showActualPreview = true"
            :loading="loadingPreview"
          >
            👁️ Lihat Preview Label
          </el-button>
        </div>

        <!-- Print Button -->
        <div style="text-align: center; margin-top: 30px;">
          <el-row :gutter="10">
            <el-col :xs="24" :sm="12" :md="12">
              <el-button type="primary" @click="printFromPreview" size="large" style="width: 100%;">
                🖨️ Print Label Ini
              </el-button>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12">
              <el-button @click="backToDashboard" size="large" style="width: 100%;">
                📋 Kembali ke Dashboard
              </el-button>
            </el-col>
          </el-row>
        </div>
      </div>

      <!-- Actual Preview Dialog -->
      <el-dialog
        v-model="showActualPreview"
        title="🖼️ Preview Label"
        :width="dialogWidth"
        append-to-body
        :fullscreen="isMobile"
      >
        <div style="text-align: center;">
          <div v-if="loadingPreview">
            <el-skeleton :rows="10" animated />
            <p>Memuat preview...</p>
          </div>
          <div v-else-if="actualPreviewUrl">
            <img 
              :src="actualPreviewUrl" 
              alt="Label Preview" 
              style="max-width: 100%; height: auto; border: 1px solid #ddd;"
            />
          </div>
          <div v-else>
            <el-empty description="Preview tidak tersedia" />
          </div>
        </div>
        
        <template #footer>
          <el-row :gutter="10">
            <el-col :xs="24" :sm="12">
              <el-button type="primary" @click="printFromPreview" style="width: 100%;">
                🖨️ Print Label Ini
              </el-button>
            </el-col>
          </el-row>
        </template>
      </el-dialog>
    </el-dialog>

    <!-- QR Scanner Component -->
    <QRScanner 
      ref="qrScannerRef"
      @scan-success="handleScanSuccess"
      @scan-error="handleScanError"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useShippingStore } from '../stores/shipping'
import { useUserStore } from '../stores/user'
import api from '../services/api'
import QRScanner from '../components/QRScanner.vue'

const router = useRouter()
const shippingStore = useShippingStore()
const userStore = useUserStore()

const shippingFormRef = ref()
const qrScannerRef = ref()
const showPreview = ref(false)
const showActualPreview = ref(false)
const generatedLabel = ref(null)
const actualPreviewUrl = ref('')
const loadingPreview = ref(false)

// Responsive design computed properties
const isMobile = computed(() => {
  return window.innerWidth < 768
})

const dialogWidth = computed(() => {
  if (window.innerWidth < 576) return '95%'
  if (window.innerWidth < 768) return '90%'
  if (window.innerWidth < 992) return '85%'
  return '80%'
})

const labelWidth = computed(() => {
  return window.innerWidth < 768 ? '100px' : '140px'
})

const labelPosition = computed(() => {
  return window.innerWidth < 576 ? 'top' : 'left'
})

const shippingForm = reactive({
  sender_name: '',
  sender_phone: '',
  recipient_name: '',
  recipient_address: '',
  recipient_phone: '',
  shipping_code: '',
  label_size: '58mm'  // Default ke 58mm
})

const shippingRules = {
  sender_name: [
    { required: true, message: 'Nama pengirim harus diisi', trigger: 'blur' }
  ],
  sender_phone: [
    { required: true, message: 'No HP pengirim harus diisi', trigger: 'blur' },
    { pattern: /^[0-9+\-\s()]{10,15}$/, message: 'Format no HP tidak valid', trigger: 'blur' }
  ],
  recipient_name: [
    // Optional field - no required validation
  ],
  recipient_address: [
    // Optional field - minimum validation only if filled
    { 
      validator: (rule, value, callback) => {
        if (value && value.length > 0 && value.length < 10) {
          callback(new Error('Alamat harus minimal 10 karakter jika diisi'))
        } else {
          callback()
        }
      }, 
      trigger: 'blur' 
    }
  ],
  recipient_phone: [
    // Optional field - format validation only if filled
    { 
      validator: (rule, value, callback) => {
        if (value && value.length > 0 && !/^[0-9+\-\s()]{10,15}$/.test(value)) {
          callback(new Error('Format no HP tidak valid'))
        } else {
          callback()
        }
      }, 
      trigger: 'blur' 
    }
  ],
  shipping_code: [
    { min: 3, message: 'Kode resi minimal 3 karakter jika diisi', trigger: 'blur' },
    { max: 50, message: 'Kode resi maksimal 50 karakter', trigger: 'blur' },
    { 
      pattern: /^[A-Za-z0-9\-_#/]*$/, 
      message: 'Kode resi hanya boleh berisi huruf, angka, -, _, #, /', 
      trigger: 'blur' 
    }
  ],
  label_size: [
    { required: true, message: 'Ukuran label harus dipilih', trigger: 'change' }
  ]
}

// Initialize form with user data
onMounted(() => {
  if (userStore.user) {
    shippingForm.sender_name = userStore.user.name
    shippingForm.sender_phone = userStore.user.phone || ''
  }
  
  // Tidak auto-generate shipping code, biarkan kosong
})

const generateShippingLabel = async () => {
  try {
    if (!shippingFormRef.value) return
    
    const valid = await shippingFormRef.value.validate()
    if (!valid) return

    const result = await shippingStore.generateShippingLabel(shippingForm)
    
    if (result.success) {
      generatedLabel.value = result.data
      showPreview.value = true
      ElMessage.success('Label pengiriman berhasil dibuat!')
    } else {
      ElMessage.error(result.error || 'Gagal membuat label pengiriman')
    }
  } catch (error) {
    console.error('Generate error:', error)
    ElMessage.error('Terjadi kesalahan saat membuat label')
  }
}

// QR Scanner functions
const openScanner = () => {
  if (qrScannerRef.value) {
    qrScannerRef.value.startScanning()
  } else {
    ElMessage.error('Scanner tidak tersedia')
  }
}

const handleScanSuccess = (scannedCode) => {
  shippingForm.shipping_code = scannedCode.toUpperCase()
  ElMessage.success(`Berhasil scan kode: ${scannedCode.toUpperCase()}`)
  
  // Clear any validation errors
  if (shippingFormRef.value) {
    shippingFormRef.value.clearValidate(['shipping_code'])
  }
}

const handleScanError = (error) => {
  ElMessage.error(`Error scanning: ${error}`)
}

// Handle shipping code input to make it uppercase
const handleShippingCodeInput = (value) => {
  shippingForm.shipping_code = value.toUpperCase()
}

const showLabelPreview = async () => {
  if (!generatedLabel.value) return
  
  try {
    loadingPreview.value = true
    const token = userStore.token
    const imageUrl = `${api.defaults.baseURL}/shipping-labels/preview/${generatedLabel.value.id}?token=${token}`
    
    // Create a promise to handle image loading
    const img = new Image()
    img.onload = () => {
      actualPreviewUrl.value = imageUrl
      loadingPreview.value = false
    }
    img.onerror = () => {
      ElMessage.error('Gagal memuat preview gambar')
      loadingPreview.value = false
    }
    img.src = imageUrl
    
  } catch (error) {
    ElMessage.error('Gagal memuat preview')
    loadingPreview.value = false
  }
}

const printFromPreview = async () => {
  try {
    if (!generatedLabel.value) {
      ElMessage.error('Tidak ada label untuk dicetak')
      return
    }

    // Detect mobile device
    const isMobileDevice = window.innerWidth <= 768 || /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
    
    if (isMobileDevice) {
      // Mobile: Show mobile-friendly options
      ElMessageBox.confirm(
        'Pilih cara mencetak label di mobile:',
        'Opsi Printing Mobile',
        {
          distinguishCancelAndClose: true,
          confirmButtonText: '📱 Buka di Tab Baru',
          cancelButtonText: '⬇️ Download PNG',
          type: 'info',
        }
      ).then(() => {
        // Open in new tab for mobile printing
        printMobileOptimized(generatedLabel.value)
      }).catch((action) => {
        if (action === 'cancel') {
          // Download image
          downloadLabelImage(generatedLabel.value)
        }
      })
    } else {
      // Desktop: Show standard options
      ElMessageBox.confirm(
        'Pilih cara mencetak label:',
        'Opsi Printing',
        {
          distinguishCancelAndClose: true,
          confirmButtonText: '🖨️ Print via Browser',
          cancelButtonText: '⬇️ Download Gambar',
          type: 'info',
        }
      ).then(() => {
        // Print via browser
        printViaBrowser(generatedLabel.value)
      }).catch((action) => {
        if (action === 'cancel') {
          // Download image
          downloadLabelImage(generatedLabel.value)
        }
      })
    }
  } catch (error) {
    ElMessage.error('Gagal mencetak label')
  }
}

const printMobileOptimized = async (label) => {
  try {
    // Get the preview image URL
    const token = userStore.token
    const imageUrl = `${api.defaults.baseURL}/shipping-labels/preview/${label.id}?token=${token}`
    const labelCode = label.shipping_code || 'Label'
    
    // Create hidden print element in current page (no popup)
    const printElement = document.createElement('div')
    printElement.id = 'hiddenMobilePrintElement'
    printElement.style.position = 'absolute'
    printElement.style.left = '-9999px'
    printElement.style.top = '0'
    printElement.style.width = label.label_size === '80mm' ? '80mm' : '58mm'
    printElement.style.height = 'auto'
    
    // Create print styles
    const printStyles = `
      <style media="print">
        @page { 
          margin: 0 !important; 
          size: ${label.label_size || '58mm'} auto !important; 
        }
        
        body * { visibility: hidden; }
        
        #hiddenMobilePrintElement, #hiddenMobilePrintElement * {
          visibility: visible;
        }
        
        #hiddenMobilePrintElement {
          position: absolute !important;
          left: 0 !important;
          top: 0 !important;
          width: ${label.label_size === '80mm' ? '80mm' : '58mm'} !important;
          margin: 0 !important;
          padding: 0 !important;
          background: white !important;
        }
        
        #hiddenMobilePrintElement img {
          width: ${label.label_size === '80mm' ? '78mm' : '56mm'} !important;
          height: auto !important;
          border: none !important;
          margin: 0 !important;
          padding: 0 !important;
          display: block !important;
        }
      </style>
    `
    
    // Add styles if not present
    if (!document.getElementById('mobilePrintStyles')) {
      const styleElement = document.createElement('div')
      styleElement.id = 'mobilePrintStyles'
      styleElement.innerHTML = printStyles
      document.head.appendChild(styleElement)
    }
    
    // Create image element
    const img = document.createElement('img')
    img.src = imageUrl
    img.alt = `Label ${labelCode}`
    img.style.width = '100%'
    img.style.height = 'auto'
    
    printElement.appendChild(img)
    document.body.appendChild(printElement)
    
    // Print when image loads
    img.onload = () => {
      setTimeout(() => {
        window.print()
        setTimeout(() => {
          if (printElement && printElement.parentNode) {
            printElement.parentNode.removeChild(printElement)
          }
        }, 1000)
      }, 500)
    }
    
    img.onerror = () => {
      ElMessage.error('Gagal memuat gambar label')
      if (printElement && printElement.parentNode) {
        printElement.parentNode.removeChild(printElement)
      }
    }
    
    ElMessage.success(`Label ${labelCode} siap dicetak!`)
    
  } catch (error) {
    ElMessage.error('Gagal mencetak label')
    console.error('Print error:', error)
  }
}

const printViaBrowser = async (label) => {
  try {
    const token = userStore.token
    const imageUrl = `${api.defaults.baseURL}/shipping-labels/preview/${label.id}?token=${token}`
    const labelCode = label.shipping_code || 'Label'
    
    // Create hidden print element (no popup)
    const printElement = document.createElement('div')
    printElement.id = 'hiddenBrowserPrintElement'
    printElement.style.position = 'absolute'
    printElement.style.left = '-9999px'
    printElement.style.top = '0'
    printElement.style.width = label.label_size === '80mm' ? '80mm' : '58mm'
    
    // Add print styles
    const printStyles = `
      <style media="print">
        @page { 
          margin: 0 !important; 
          size: ${label.label_size || '58mm'} auto !important; 
        }
        
        body * { visibility: hidden; }
        
        #hiddenBrowserPrintElement, #hiddenBrowserPrintElement * {
          visibility: visible;
        }
        
        #hiddenBrowserPrintElement {
          position: absolute !important;
          left: 0 !important;
          top: 0 !important;
          width: ${label.label_size === '80mm' ? '80mm' : '58mm'} !important;
          margin: 0 !important;
          padding: 0 !important;
          background: white !important;
        }
        
        #hiddenBrowserPrintElement img {
          width: ${label.label_size === '80mm' ? '78mm' : '56mm'} !important;
          height: auto !important;
          border: none !important;
          margin: 0 !important;
          padding: 0 !important;
          display: block !important;
        }
      </style>
    `
    
    if (!document.getElementById('browserPrintStyles')) {
      const styleElement = document.createElement('div')
      styleElement.id = 'browserPrintStyles'
      styleElement.innerHTML = printStyles
      document.head.appendChild(styleElement)
    }
    
    const img = document.createElement('img')
    img.src = imageUrl
    img.alt = `Label ${labelCode}`
    img.style.width = '100%'
    img.style.height = 'auto'
    
    printElement.appendChild(img)
    document.body.appendChild(printElement)
    
    img.onload = () => {
      setTimeout(() => {
        window.print()
        setTimeout(() => {
          if (printElement && printElement.parentNode) {
            printElement.parentNode.removeChild(printElement)
          }
        }, 1000)
      }, 500)
    }
    
    img.onerror = () => {
      ElMessage.error('Gagal memuat gambar label')
      if (printElement && printElement.parentNode) {
        printElement.parentNode.removeChild(printElement)
      }
    }
    
    ElMessage.success(`Label ${labelCode} siap dicetak!`)
    
  } catch (error) {
    ElMessage.error('Gagal mencetak label')
    console.error('Print error:', error)
  }
}

const downloadLabelImage = async (label) => {
  try {
    const token = userStore.token
    const imageUrl = `${api.defaults.baseURL}/shipping-labels/preview/${label.id}?token=${token}`
    
    const link = document.createElement('a')
    link.href = imageUrl
    link.download = `shipping_label_${label.shipping_code}.png`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    ElMessage.success(`Label pengiriman ${label.shipping_code} berhasil didownload!`)
    
    showPreview.value = false
    setTimeout(() => {
      router.push('/dashboard')
    }, 1500)
  } catch (error) {
    ElMessage.error('Gagal download label')
    console.error('Download error:', error)
  }
}

const handleClosePreview = () => {
  showPreview.value = false
  showActualPreview.value = false
  actualPreviewUrl.value = ''
}

const backToDashboard = () => {
  showPreview.value = false
  router.push('/dashboard')
}

const resetShippingForm = () => {
  // Reset all form fields
  Object.keys(shippingForm).forEach(key => {
    if (key === 'sender_name' && userStore.user?.name) {
      shippingForm[key] = userStore.user.name
    } else if (key === 'sender_phone' && userStore.user?.phone) {
      shippingForm[key] = userStore.user.phone
    } else if (key === 'label_size') {
      shippingForm[key] = '58mm'  // Reset to default size
    } else {
      shippingForm[key] = ''
    }
  })
  
  // Clear any validation errors
  if (shippingFormRef.value) {
    shippingFormRef.value.clearValidate()
  }
  
  shippingStore.clearError()
  ElMessage.success('Form berhasil direset!')
}

const resetForm = () => {
  // Keep sender info, reset only recipient and shipping code
  shippingForm.recipient_name = ''
  shippingForm.recipient_address = ''
  shippingForm.recipient_phone = ''
  shippingForm.shipping_code = '' // Reset to empty, tidak auto-generate
  
  shippingStore.clearError()
}

// Watch for showActualPreview to load image
import { watch } from 'vue'
watch(showActualPreview, (newValue) => {
  if (newValue && generatedLabel.value) {
    showLabelPreview()
  }
})
</script>

<style scoped>
.create-shipping-label-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 10px;
  min-height: 100vh;
}

/* Shipping Button Group Layout */
.shipping-button-group {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
  width: 100%;
  margin-top: 20px;
}

/* Desktop/Tablet Layout */
@media (min-width: 769px) {
  .shipping-button-group {
    flex-direction: row;
    justify-content: space-between;
  }
  
  .shipping-action-button {
    flex: 1;
    max-width: 200px;
  }
}

.shipping-action-button {
  flex: 1;
  min-width: 120px;
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.shipping-primary-button {
  background: linear-gradient(135deg, #409EFF, #67C23A);
  border: none;
  color: white;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.shipping-primary-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(64, 158, 255, 0.4);
}

.shipping-secondary-button {
  background: #F5F7FA;
  border: 2px solid #E4E7ED;
  color: #606266;
}

.shipping-secondary-button:hover {
  background: #E4E7ED;
  border-color: #C0C4CC;
}

.shipping-info-button {
  background: #909399;
  border: none;
  color: white;
}

.shipping-info-button:hover {
  background: #82868A;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  color: #409eff;
  font-size: 1.1rem;
}

.preview-content {
  max-height: 60vh;
  overflow-y: auto;
}

:deep(.el-divider__text) {
  background-color: #f5f7fa;
  padding: 0 20px;
  font-size: 0.9rem;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266;
}

:deep(.el-textarea__inner) {
  font-family: inherit;
}

:deep(.el-card__header) {
  padding: 12px 20px;
}

:deep(.el-card__body) {
  padding: 15px 20px;
}

/* Mobile Responsiveness - Full Width */
@media (max-width: 768px) {
  .create-shipping-label-container {
    padding: 3px !important;
    margin: 0 !important;
    max-width: 100% !important;
    width: 100% !important;
  }
  
  .card-header {
    font-size: 1rem;
    flex-direction: column;
    text-align: center;
  }
  
  .preview-content {
    max-height: 70vh;
  }
  
  :deep(.el-card) {
    margin: 0 !important;
    border-radius: 8px;
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box;
  }
  
  :deep(.el-card__body) {
    padding: 15px;
  }
  
  :deep(.el-form-item) {
    margin-bottom: 18px;
  }
  
  :deep(.el-form-item__label) {
    font-size: 14px;
    font-weight: 500;
    width: 120px !important;
  }
  
  :deep(.el-form-item__content) {
    flex: 1;
  }
  
  :deep(.el-input) {
    width: 100%;
  }
  
  :deep(.el-input__wrapper) {
    width: 100%;
  }
  
  :deep(.el-input__inner) {
    font-size: 16px; /* Prevents zoom on iOS */
    padding: 12px 15px;
    width: 100%;
    box-sizing: border-box;
  }
  
  :deep(.el-textarea__inner) {
    font-size: 16px; /* Prevents zoom on iOS */
    padding: 12px 15px;
    width: 100%;
    box-sizing: border-box;
  }
  
  :deep(.el-input-group__append .el-button) {
    padding: 12px 15px;
    font-size: 14px;
  }
  
  :deep(.el-button) {
    font-size: 14px;
    padding: 12px 15px;
    box-sizing: border-box;
  }
  
  /* Shipping Button Group Mobile Layout */
  .shipping-button-group {
    flex-direction: column;
    gap: 8px;
    margin-top: 15px;
  }
  
  .shipping-action-button {
    width: 100% !important;
    min-width: unset;
    margin-bottom: 8px;
    font-size: 14px;
    padding: 12px 16px;
    min-height: 44px;
  }
  
  :deep(.el-divider__text) {
    font-size: 0.85rem;
    padding: 0 15px;
  }
  
  :deep(.el-card__header) {
    padding: 10px 15px;
  }
}

@media (max-width: 576px) {
  .create-shipping-label-container {
    padding: 3px;
  }
  
  .card-header {
    font-size: 0.95rem;
  }
  
  /* Compact shipping button layout for small screens */
  .shipping-button-group {
    gap: 6px;
    margin-top: 12px;
  }
  
  .shipping-action-button {
    font-size: 13px;
    padding: 10px 12px;
    min-height: 42px;
  }
  
  .preview-content {
    max-height: 75vh;
  }
  
  :deep(.el-card__body) {
    padding: 12px;
  }
  
  :deep(.el-form-item__label) {
    font-size: 13px;
    margin-bottom: 5px;
    width: 110px !important;
  }
  
  :deep(.el-input__inner) {
    font-size: 16px;
    padding: 10px 12px;
  }
  
  :deep(.el-textarea__inner) {
    font-size: 16px;
    padding: 10px 12px;
  }
  
  :deep(.el-input-group__append .el-button) {
    padding: 10px 12px;
    font-size: 13px;
  }
  
  :deep(.el-button) {
    font-size: 13px;
    padding: 10px 12px;
  }
  
  :deep(.el-divider__text) {
    font-size: 0.8rem;
    padding: 0 10px;
  }
  
  :deep(.el-card__header) {
    padding: 8px 10px;
    font-size: 0.9rem;
  }
  
  :deep(.el-card__body p) {
    font-size: 0.85rem;
    margin: 3px 0;
  }
  
  :deep(.el-form-item) {
    margin-bottom: 15px;
  }
}

@media (max-width: 480px) {
  .create-shipping-label-container {
    padding: 2px;
  }
  
  :deep(.el-card) {
    margin: 0;
  }
  
  :deep(.el-card__body) {
    padding: 10px;
  }
  
  :deep(.el-form-item__label) {
    width: 100px !important;
    font-size: 12px;
  }
  
  :deep(.el-input-group__append .el-button) {
    padding: 8px 10px;
    font-size: 12px;
  }
  
  :deep(.el-input-group__append) {
    border-radius: 0 4px 4px 0;
  }
}

/* Form label positioning for mobile */
@media (max-width: 576px) {
  :deep(.el-form-item__label) {
    padding: 0 !important;
    line-height: 1.4;
  }
  
  :deep(.el-form-item__content) {
    margin-left: 0 !important;
  }
}

/* Dialog responsiveness */
@media (max-width: 768px) {
  :deep(.el-dialog) {
    margin: 10px !important;
    max-height: calc(100vh - 20px);
    width: calc(100vw - 20px) !important;
  }
  
  :deep(.el-dialog__body) {
    padding: 15px;
    max-height: calc(100vh - 150px);
    overflow-y: auto;
  }
  
  :deep(.el-dialog__footer) {
    padding: 15px;
  }
}

/* Landscape mobile */
@media (max-width: 896px) and (orientation: landscape) and (max-height: 500px) {
  .create-shipping-label-container {
    padding: 3px;
  }
  
  :deep(.el-card__body) {
    padding: 8px;
  }
  
  .card-header {
    font-size: 0.9rem;
  }
  
  :deep(.el-divider__text) {
    font-size: 0.75rem;
    padding: 0 8px;
  }
  
  :deep(.el-form-item) {
    margin-bottom: 10px;
  }
}

/* Label Size Radio Group Styles */
.label-size-group {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
  margin: 10px 0;
}

:deep(.label-size-group .el-radio-button) {
  flex: 1;
  min-width: 140px;
  max-width: 200px;
}

:deep(.label-size-group .el-radio-button__inner) {
  width: 100%;
  height: 80px;
  border-radius: 12px;
  border: 2px solid #dcdfe6;
  background: #fafafa;
  padding: 12px 16px;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  font-weight: 500;
}

:deep(.label-size-group .el-radio-button__inner:hover) {
  border-color: #409eff;
  background: #f0f8ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.15);
}

:deep(.label-size-group .el-radio-button.is-active .el-radio-button__inner) {
  border-color: #409eff;
  background: linear-gradient(135deg, #409eff, #66b3ff);
  color: white;
  box-shadow: 0 6px 16px rgba(64, 158, 255, 0.3);
  transform: translateY(-2px);
}

.radio-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 4px;
}

.radio-title {
  font-size: 16px;
  font-weight: 600;
  line-height: 1.2;
}

.radio-description {
  font-size: 12px;
  opacity: 0.8;
  line-height: 1.2;
}

:deep(.label-size-group .el-radio-button.is-active .radio-description) {
  opacity: 0.9;
}

/* Mobile responsive for label size */
@media (max-width: 480px) {
  .label-size-group {
    flex-direction: column;
    gap: 10px;
  }
  
  :deep(.label-size-group .el-radio-button) {
    max-width: 100%;
  }
  
  :deep(.label-size-group .el-radio-button__inner) {
    height: 70px;
    padding: 10px 12px;
  }
  
  .radio-title {
    font-size: 14px;
  }
  
  .radio-description {
    font-size: 11px;
  }
}
</style>