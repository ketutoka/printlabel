<template>
  <div class="create-shipping-label-container">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>📦 Buat Label Pengiriman</span>
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
          <span style="color: #67c23a; font-weight: bold;">📥 PENERIMA</span>
        </el-divider>

        <el-form-item label="Nama Penerima" prop="recipient_name">
          <el-input 
            v-model="shippingForm.recipient_name" 
            placeholder="Nama lengkap penerima"
            clearable
          />
        </el-form-item>

        <el-form-item label="Alamat Lengkap" prop="recipient_address">
          <el-input 
            v-model="shippingForm.recipient_address" 
            type="textarea"
            :rows="3"
            placeholder="Alamat lengkap penerima (jalan, RT/RW, kelurahan, kecamatan, kota, provinsi, kode pos)"
            clearable
          />
        </el-form-item>

        <el-form-item label="No HP Penerima" prop="recipient_phone">
          <el-input 
            v-model="shippingForm.recipient_phone" 
            placeholder="Contoh: 081234567890"
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

        <el-form-item>
          <el-row :gutter="10" style="margin-top: 20px;">
            <el-col :xs="24" :sm="12" :md="12">
              <el-button 
                type="primary" 
                @click="generateShippingLabel"
                :loading="shippingStore.loading"
                size="large"
                style="width: 100%;"
              >
                <span v-if="!shippingStore.loading">🏷️ Buat Label</span>
                <span v-else>⏳ Membuat Label...</span>
              </el-button>
            </el-col>
            <el-col :xs="24" :sm="12" :md="12">
              <el-button 
                type="info" 
                @click="backToDashboard"
                size="large"
                style="width: 100%;"
              >
                ← Kembali
              </el-button>
            </el-col>
          </el-row>          
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
  shipping_code: ''
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
    { required: true, message: 'Nama penerima harus diisi', trigger: 'blur' }
  ],
  recipient_address: [
    { required: true, message: 'Alamat penerima harus diisi', trigger: 'blur' },
    { min: 10, message: 'Alamat harus minimal 10 karakter', trigger: 'blur' }
  ],
  recipient_phone: [
    { required: true, message: 'No HP penerima harus diisi', trigger: 'blur' },
    { pattern: /^[0-9+\-\s()]{10,15}$/, message: 'Format no HP tidak valid', trigger: 'blur' }
  ],
  shipping_code: [
    { min: 3, message: 'Kode resi minimal 3 karakter jika diisi', trigger: 'blur' },
    { max: 50, message: 'Kode resi maksimal 50 karakter', trigger: 'blur' },
    { 
      pattern: /^[A-Za-z0-9\-_#/]*$/, 
      message: 'Kode resi hanya boleh berisi huruf, angka, -, _, #, /', 
      trigger: 'blur' 
    }
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
  shippingForm.shipping_code = scannedCode
  ElMessage.success(`Berhasil scan kode: ${scannedCode}`)
  
  // Clear any validation errors
  if (shippingFormRef.value) {
    shippingFormRef.value.clearValidate(['shipping_code'])
  }
}

const handleScanError = (error) => {
  ElMessage.error(`Error scanning: ${error}`)
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

    // Show print options dialog
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
  } catch (error) {
    ElMessage.error('Gagal mencetak label')
  }
}

const printViaBrowser = async (label) => {
  try {
    const token = userStore.token
    const imageUrl = `${api.defaults.baseURL}/shipping-labels/preview/${label.id}?token=${token}`
    
    const printWindow = window.open('', '_blank')
    printWindow.document.write(`
      <!DOCTYPE html>
      <html>
      <head>
        <title>Print Shipping Label - ${label.shipping_code}</title>
        <style>
          @page {
            margin: 0;
            size: 58mm auto;
          }
          body {
            margin: 0;
            padding: 5mm;
            font-family: Arial, sans-serif;
          }
          img {
            width: 100%;
            height: auto;
            max-width: 48mm;
          }
          @media print {
            body {
              padding: 0;
            }
            img {
              max-width: 58mm;
            }
          }
        </style>
      </head>
      <body>
        <img src="${imageUrl}" alt="Shipping Label ${label.shipping_code}" onload="window.print(); window.close();" />
      </body>
      </html>
    `)
    printWindow.document.close()
    
    ElMessage.success(`Label pengiriman ${label.shipping_code} dikirim ke printer!`)
    
    showPreview.value = false
    setTimeout(() => {
      router.push('/dashboard')
    }, 1500)
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
  max-width: 800px;
  margin: 0 auto;
  padding: 20px 15px;
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

/* Mobile optimizations */
@media (max-width: 768px) {
  .create-shipping-label-container {
    padding: 15px 10px;
  }
  
  .card-header {
    font-size: 1rem;
    flex-direction: column;
    text-align: center;
  }
  
  .preview-content {
    max-height: 70vh;
  }
  
  :deep(.el-divider__text) {
    font-size: 0.85rem;
    padding: 0 15px;
  }
  
  :deep(.el-card__header) {
    padding: 10px 15px;
  }
  
  :deep(.el-card__body) {
    padding: 12px 15px;
  }
  
  :deep(.el-form-item) {
    margin-bottom: 15px;
  }
}

@media (max-width: 576px) {
  .create-shipping-label-container {
    padding: 10px 5px;
  }
  
  .card-header {
    font-size: 0.95rem;
  }
  
  .preview-content {
    max-height: 75vh;
  }
  
  :deep(.el-divider__text) {
    font-size: 0.8rem;
    padding: 0 10px;
  }
  
  :deep(.el-card__header) {
    padding: 8px 10px;
    font-size: 0.9rem;
  }
  
  :deep(.el-card__body) {
    padding: 10px;
  }
  
  :deep(.el-card__body p) {
    font-size: 0.85rem;
    margin: 3px 0;
  }
  
  :deep(.el-form-item) {
    margin-bottom: 12px;
  }
  
  :deep(.el-form-item__label) {
    font-size: 0.9rem;
  }
  
  :deep(.el-input__inner) {
    font-size: 0.9rem;
  }
  
  :deep(.el-textarea__inner) {
    font-size: 0.9rem;
  }
  
  :deep(.el-button) {
    font-size: 0.85rem;
  }
}

/* Very small screens */
@media (max-width: 480px) {
  .create-shipping-label-container {
    padding: 5px;
  }
  
  :deep(.el-card) {
    margin: 0;
  }
  
  :deep(.el-card__body) {
    padding: 8px;
  }
  
  :deep(.el-form-item__label) {
    font-size: 0.85rem;
  }
}
</style>