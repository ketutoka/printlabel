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
        label-width="140px"
        label-position="left"
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
            placeholder="Kosongkan jika tidak ada kode resi"
            clearable
          />
          <div style="font-size: 12px; color: #909399; margin-top: 5px;">
            💡 Tips: Kode resi akan disembunyikan jika dikosongkan
          </div>
        </el-form-item>

        <el-form-item>
          <el-button 
            type="primary" 
            @click="generateShippingLabel"
            :loading="shippingStore.loading"
            size="large"
            style="width: 100%; margin-top: 20px;"
          >
            <span v-if="!shippingStore.loading">🏷️ Buat Label Pengiriman</span>
            <span v-else>⏳ Membuat Label...</span>
          </el-button>
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
      width="90%"
      :before-close="handleClosePreview"
    >
      <div v-if="generatedLabel" class="preview-content">
        <!-- Label Details -->
        <el-row :gutter="20" style="margin-bottom: 20px;">
          <el-col :span="12">
            <el-card shadow="never">
              <template #header>
                <span>📤 Pengirim</span>
              </template>
              <p><strong>Nama:</strong> {{ generatedLabel.sender_name }}</p>
              <p><strong>No HP:</strong> {{ generatedLabel.sender_phone }}</p>
            </el-card>
          </el-col>
          <el-col :span="12">
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
          <el-button type="primary" @click="printFromPreview" size="large">
            🖨️ Print Label Ini
          </el-button>
          <el-button @click="backToDashboard" size="large">
            📋 Kembali ke Dashboard
          </el-button>
        </div>
      </div>

      <!-- Actual Preview Dialog -->
      <el-dialog
        v-model="showActualPreview"
        title="🖼️ Preview Label"
        width="400px"
        append-to-body
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
          <el-button type="primary" @click="printFromPreview">
            🖨️ Print Label Ini
          </el-button>
        </template>
      </el-dialog>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useShippingStore } from '../stores/shipping'
import { useUserStore } from '../stores/user'
import api from '../services/api'

const router = useRouter()
const shippingStore = useShippingStore()
const userStore = useUserStore()

const shippingFormRef = ref()
const showPreview = ref(false)
const showActualPreview = ref(false)
const generatedLabel = ref(null)
const actualPreviewUrl = ref('')
const loadingPreview = ref(false)

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
    { min: 3, message: 'Kode resi minimal 3 karakter jika diisi', trigger: 'blur' }
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
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  color: #409eff;
}

.preview-content {
  max-height: 60vh;
  overflow-y: auto;
}

:deep(.el-divider__text) {
  background-color: #f5f7fa;
  padding: 0 20px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266;
}

:deep(.el-textarea__inner) {
  font-family: inherit;
}
</style>