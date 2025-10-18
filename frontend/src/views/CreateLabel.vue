<template>
  <div class="create-label-container">
    <div class="form-wrapper">
      <el-card shadow="hover" class="mobile-card">
          <template #header>
            <div class="card-header">
              <h2>🏷️ Buat QRCODE Label</h2>
              <p>Isi informasi untuk membuat label paket dengan QR Code</p>
            </div>
          </template>

          <el-form
            ref="labelFormRef"
            :model="labelForm"
            :rules="rules"
            :label-width="labelWidth"
            :label-position="labelPosition"
            @submit.prevent="handleCreateLabel"
          >
            <el-form-item label="Nama" prop="sender_name">
              <el-input
                v-model="labelForm.sender_name"
                placeholder="Masukkan nama pengirim"
                prefix-icon="User"
              />
            </el-form-item>

            <el-form-item label="No HP" prop="sender_phone">
              <el-input
                v-model="labelForm.sender_phone"
                placeholder="Masukkan nomor HP pengirim"
                prefix-icon="Phone"
              />
            </el-form-item>

            <el-form-item label="Resi" prop="shipping_code">
              <el-input
                v-model="labelForm.shipping_code"
                placeholder="Scan QR Code/Barcode atau ketik manual"
                prefix-icon="DocumentCopy"
              >
                <template #append>
                  <el-button 
                    type="primary" 
                    @click="openScanner"
                    icon="CameraFilled"
                  >
                    Scan
                  </el-button>
                </template>
              </el-input>
            </el-form-item>

            <el-form-item>
              <div class="button-group">
                <el-button
                  type="primary"
                  :loading="labelStore.loading"
                  @click="handleCreateLabel"
                  size="large"
                  class="action-button primary-button"
                >
                  {{ labelStore.loading ? 'Membuat Label...' : '🏷️ Buat QR' }}
                </el-button>
                <el-button 
                  @click="resetForm" 
                  size="large"
                  class="action-button secondary-button"
                >
                  🔄 Reset
                </el-button>
                <el-button 
                  type="info" 
                  @click="$router.push('/dashboard')" 
                  size="large"
                  class="action-button info-button"
                >
                  ⬅️ Kembali
                </el-button>
              </div>
            </el-form-item>
          </el-form>

          <!-- Error Alert -->
          <el-alert
            v-if="labelStore.error"
            :title="labelStore.error"
            type="error"
            style="margin-top: 15px"
            show-icon
            @close="labelStore.clearError"
          />
        </el-card>
    </div>

    <!-- QR Scanner Component -->
    <QRScanner 
      ref="qrScannerRef"
      @scan-success="handleScanSuccess"
      @scan-error="handleScanError"
    />

    <!-- Preview Modal -->
    <el-dialog
      v-model="showPreview"
      title="Preview Label"
      :width="dialogWidth"
      center
      :fullscreen="isMobile"
    >
      <div v-if="generatedLabel" class="label-preview">
        <div class="preview-header">
          <h3>🏷️ LABEL PENGIRIMAN</h3>
        </div>
        
        <el-divider />
        
        <div class="preview-content">
          <p><strong>Pengirim:</strong></p>
          <p>{{ generatedLabel.sender_name }}</p>
          
          <p style="margin-top: 10px;"><strong>No HP:</strong></p>
          <p>{{ labelForm.sender_phone || 'Tidak ada' }}</p>
          
          <p style="margin-top: 15px;"><strong>Kode Pengiriman:</strong></p>
          <p>{{ generatedLabel.shipping_code }}</p>
          
          <div class="qr-placeholder">
            <p>📱 QR Code</p>
            <small>{{ generatedLabel.shipping_code }}</small>
          </div>
          
          <p style="margin-top: 15px; font-size: 12px;">
            Tanggal: {{ formatDate(generatedLabel.created_at) }}
          </p>
        </div>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-row :gutter="10">
            <el-col :xs="12" :sm="6">
              <el-button @click="showPreview = false" style="width: 100%;">Tutup</el-button>
            </el-col>
            <el-col :xs="12" :sm="6">
              <el-button 
                type="success" 
                @click="previewActualLabel"
                style="width: 100%;"
              >
                👁️ Preview
              </el-button>
            </el-col>
            <el-col :xs="12" :sm="6">
              <el-button type="primary" @click="printLabel" style="width: 100%;">
                🖨️ Print
              </el-button>
            </el-col>
            <el-col :xs="12" :sm="6">
              <el-button type="info" @click="createAnotherLabel" style="width: 100%;">
                Buat Lagi
              </el-button>
            </el-col>
          </el-row>
        </div>
      </template>
    </el-dialog>

    <!-- Actual Label Preview Dialog -->
    <el-dialog
      v-model="showActualPreview"
      title="Preview Label Asli"
      :width="dialogWidth"
      center
      :fullscreen="isMobile"
    >
      <div v-if="generatedLabel" class="actual-preview-container">
        <div class="preview-info">
          <h3>🏷️ {{ generatedLabel.shipping_code }}</h3>
          <p><strong>Pengirim:</strong> {{ generatedLabel.sender_name }}</p>
          <p><strong>No HP:</strong> {{ labelForm.sender_phone || 'Tidak ada' }}</p>
          <p><strong>Tanggal:</strong> {{ formatDate(generatedLabel.created_at) }}</p>
        </div>
        
        <div class="actual-image-container">
          <img 
            :src="actualPreviewUrl" 
            alt="Label Preview Asli"
            class="actual-preview-image"
            @error="handlePreviewError"
          />
        </div>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-row :gutter="10">
            <el-col :xs="12" :sm="12">
              <el-button @click="showActualPreview = false" style="width: 100%;">Tutup</el-button>
            </el-col>
            <el-col :xs="12" :sm="12">
              <el-button type="primary" @click="printFromPreview" style="width: 100%;">
                🖨️ Print Label Ini
              </el-button>
            </el-col>
          </el-row>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useLabelStore } from '../stores/label'
import { useUserStore } from '../stores/user'
import api from '../services/api'
import QRScanner from '../components/QRScanner.vue'

const router = useRouter()
const labelStore = useLabelStore()
const userStore = useUserStore()

const labelFormRef = ref()
const qrScannerRef = ref()
const showPreview = ref(false)
const showActualPreview = ref(false)
const generatedLabel = ref(null)
const actualPreviewUrl = ref('')

// Responsive design computed properties
const isMobile = computed(() => {
  return window.innerWidth < 768
})

const dialogWidth = computed(() => {
  if (window.innerWidth < 576) return '95%'
  if (window.innerWidth < 768) return '90%'
  if (window.innerWidth < 992) return '80%'
  return '600px'
})

const labelWidth = computed(() => {
  return window.innerWidth < 768 ? '90px' : '120px'
})

const labelPosition = computed(() => {
  return window.innerWidth < 576 ? 'top' : 'right'
})

const labelForm = reactive({
  sender_name: '',
  sender_phone: '',
  shipping_code: ''
})

const rules = {
  sender_name: [
    { required: true, message: 'Nama pengirim harus diisi', trigger: 'blur' },
    { min: 2, message: 'Nama pengirim minimal 2 karakter', trigger: 'blur' }
  ],
  sender_phone: [
    { required: true, message: 'No HP pengirim harus diisi', trigger: 'blur' },
    { 
      pattern: /^[0-9+\-\s()]+$/, 
      message: 'No HP hanya boleh berisi angka, +, -, spasi, dan tanda kurung', 
      trigger: 'blur' 
    },
    { min: 8, message: 'No HP minimal 8 karakter', trigger: 'blur' },
    { max: 20, message: 'No HP maksimal 20 karakter', trigger: 'blur' }
  ],
  shipping_code: [
    { required: true, message: 'Kode pengiriman harus diisi', trigger: 'blur' },
    { min: 3, message: 'Kode pengiriman minimal 3 karakter', trigger: 'blur' },
    { max: 50, message: 'Kode pengiriman maksimal 50 karakter', trigger: 'blur' },
    { 
      pattern: /^[A-Za-z0-9\-_#/]+$/, 
      message: 'Kode pengiriman hanya boleh berisi huruf, angka, -, _, #, /', 
      trigger: 'blur' 
    }
  ]
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
  labelForm.shipping_code = scannedCode
  ElMessage.success(`Berhasil scan kode: ${scannedCode}`)
  
  // Clear any validation errors
  if (labelFormRef.value) {
    labelFormRef.value.clearValidate(['shipping_code'])
  }
}

const handleScanError = (error) => {
  ElMessage.error(`Error scanning: ${error}`)
}

const handleCreateLabel = async () => {
  if (!labelFormRef.value) return
  
  await labelFormRef.value.validate(async (valid) => {
    if (valid) {
      const result = await labelStore.createLabel(labelForm)
      
      if (result.success) {
        generatedLabel.value = result.data
        showPreview.value = true
        ElMessage.success('Label berhasil dibuat!')
      } else {
        ElMessage.error(result.error || 'Gagal membuat label')
      }
    }
  })
}

const resetForm = () => {
  // Reset to default values from user profile
  labelForm.sender_name = userStore.user?.name || ''
  labelForm.sender_phone = userStore.user?.phone || ''
  labelForm.shipping_code = ''
  labelStore.clearError()
}

// Initialize form with user data
onMounted(() => {
  // Set default values from user profile
  labelForm.sender_name = userStore.user?.name || ''
  labelForm.sender_phone = userStore.user?.phone || ''
})

const printLabel = async () => {
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
    const imageUrl = `${api.defaults.baseURL}/labels/preview/${label.id}?token=${token}`
    
    // Create a mobile-optimized print page
    const printWindow = window.open('', '_blank')
    printWindow.document.write(`
      <!DOCTYPE html>
      <html>
      <head>
        <title>Label ${label.shipping_code}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
          * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
          }
          
          body {
            font-family: Arial, sans-serif;
            padding: 10px;
            background: #f5f5f5;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
          }
          
          .mobile-print-container {
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            max-width: 350px;
            width: 100%;
            text-align: center;
          }
          
          h2 {
            color: #409EFF;
            margin-bottom: 15px;
            font-size: 18px;
          }
          
          .label-info {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 6px;
            margin-bottom: 15px;
            text-align: left;
          }
          
          .label-info p {
            margin: 5px 0;
            font-size: 14px;
            color: #666;
          }
          
          .label-image {
            width: 100%;
            max-width: 300px;
            height: auto;
            border: 2px dashed #409EFF;
            border-radius: 8px;
            padding: 10px;
            background: white;
            margin: 15px 0;
          }
          
          .print-actions {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            justify-content: center;
            margin-top: 20px;
          }
          
          .btn {
            padding: 12px 20px;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            min-width: 120px;
            text-align: center;
            transition: all 0.3s ease;
          }
          
          .btn-primary {
            background: #409EFF;
            color: white;
          }
          
          .btn-primary:hover {
            background: #337ecc;
          }
          
          .btn-success {
            background: #67C23A;
            color: white;
          }
          
          .btn-success:hover {
            background: #529b2e;
          }
          
          .print-instructions {
            background: #e1f3d8;
            padding: 10px;
            border-radius: 6px;
            margin-top: 15px;
            font-size: 12px;
            color: #529b2e;
            text-align: left;
          }
          
          @media print {
            body {
              background: white;
              padding: 0;
            }
            
            .print-actions,
            .print-instructions {
              display: none !important;
            }
            
            .mobile-print-container {
              box-shadow: none;
              border: none;
              width: 58mm;
              max-width: 58mm;
            }
            
            .label-image {
              width: 54mm;
              max-width: 54mm;
              border: none;
              padding: 0;
            }
          }
        </style>
      </head>
      <body>
        <div class="mobile-print-container">
          <h2>🏷️ Label Pengiriman</h2>
          
          <div class="label-info">
            <p><strong>Kode:</strong> ${label.shipping_code}</p>
            <p><strong>Pengirim:</strong> ${label.sender_name || 'Tidak ada'}</p>
            <p><strong>Tanggal:</strong> ${new Date(label.created_at).toLocaleDateString('id-ID')}</p>
          </div>
          
          <img src="${imageUrl}" alt="Label ${label.shipping_code}" class="label-image" />
          
          <div class="print-actions">
            <button class="btn btn-primary" onclick="window.print()">🖨️ Print</button>
            <a href="${imageUrl}" download="label_${label.shipping_code}.png" class="btn btn-success">⬇️ Download</a>
          </div>
          
          <div class="print-instructions">
            <strong>📱 Cara Print di Mobile:</strong><br>
            1. Tekan tombol "Print" di atas<br>
            2. Pilih printer atau "Save as PDF"<br>
            3. Untuk thermal printer, pastikan ukuran kertas 58mm<br>
            4. Atau download gambar dan print dari aplikasi foto
          </div>
        </div>
      </body>
      </html>
    `)
    printWindow.document.close()
    
    ElMessage.success(`Label ${label.shipping_code} dibuka di tab baru untuk printing`)
  } catch (error) {
    ElMessage.error('Gagal membuka halaman print mobile')
    console.error('Mobile print error:', error)
  }
}

const printViaBrowser = async (label) => {
  try {
    // Get the preview image URL
    const token = userStore.token
    const imageUrl = `${api.defaults.baseURL}/labels/preview/${label.id}?token=${token}`
    
    // Create a new window for printing
    const printWindow = window.open('', '_blank')
    printWindow.document.write(`
      <!DOCTYPE html>
      <html>
      <head>
        <title>Print Label - ${label.shipping_code}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
          * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
          }
          
          @page {
            margin: 0;
            size: 58mm 100mm;
            orientation: portrait;
          }
          
          html, body {
            margin: 0;
            padding: 0;
            width: 58mm;
            height: 100mm;
            overflow: hidden;
            background: white;
          }
          
          .print-container {
            width: 58mm;
            height: auto;
            max-height: 100mm;
            padding: 2mm;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
          }
          
          img {
            width: 54mm;
            height: auto;
            max-width: 54mm;
            display: block;
            object-fit: contain;
          }
          
          @media print {
            html, body {
              width: 58mm !important;
              height: 100mm !important;
              overflow: hidden !important;
            }
            
            .print-container {
              padding: 1mm !important;
            }
            
            img {
              width: 56mm !important;
              max-width: 56mm !important;
              page-break-inside: avoid;
            }
          }
          
          /* Mobile print optimization */
          @media screen and (max-width: 768px) {
            body {
              padding: 5px;
              height: auto;
            }
            
            .print-container {
              width: 100%;
              max-width: 300px;
              margin: 0 auto;
            }
            
            img {
              width: 100%;
              max-width: 280px;
            }
          }
        </style>
      </head>
      <body>
        <div class="print-container">
          <img src="${imageUrl}" alt="Label ${label.shipping_code}" onload="setTimeout(() => { window.print(); setTimeout(() => window.close(), 1000); }, 500);" onerror="alert('Gagal memuat gambar label');" />
        </div>
      </body>
      </html>
    `)
    printWindow.document.close()
    
    ElMessage.success(`Label ${label.shipping_code} dikirim ke printer!`)
    
    // Close preview and redirect after successful print
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
    const imageUrl = `${api.defaults.baseURL}/labels/preview/${label.id}?token=${token}`
    
    // Create download link
    const link = document.createElement('a')
    link.href = imageUrl
    link.download = `label_${label.shipping_code}.png`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    ElMessage.success(`Label ${label.shipping_code} berhasil didownload!`)
    
    // Close preview and redirect after download
    showPreview.value = false
    setTimeout(() => {
      router.push('/dashboard')
    }, 1500)
  } catch (error) {
    ElMessage.error('Gagal download label')
    console.error('Download error:', error)
  }
}

const createAnotherLabel = () => {
  showPreview.value = false
  showActualPreview.value = false
  resetForm()
  ElMessage.info('Silakan buat label baru')
}

const previewActualLabel = async () => {
  try {
    if (generatedLabel.value && generatedLabel.value.id) {
      ElMessage.info('Memuat preview label asli...')
      
      actualPreviewUrl.value = await labelStore.getPreviewUrl(generatedLabel.value.id)
      showActualPreview.value = true
      
      ElMessage.success('Preview label asli berhasil dimuat')
    }
  } catch (error) {
    console.error('Preview error:', error)
    ElMessage.error('Gagal memuat preview label asli')
  }
}

const printFromPreview = async () => {
  try {
    ElMessage.success(`Label ${generatedLabel.value.shipping_code} berhasil dicetak!`)
    showActualPreview.value = false
    showPreview.value = false
    
    setTimeout(() => {
      router.push('/dashboard')
    }, 1000)
  } catch (error) {
    ElMessage.error('Gagal mencetak label')
  }
}

const handlePreviewError = () => {
  ElMessage.error('Gagal memuat gambar preview')
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('id-ID', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.create-label-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 10px;
  min-height: 100vh;
  width: 100%;
}

.form-wrapper {
  width: 100%;
}

.mobile-card {
  width: 100%;
}

/* Button Group Layout */
.button-group {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
  width: 100%;
  margin-top: 10px;
}

/* Desktop/Tablet Layout */
@media (min-width: 769px) {
  .button-group {
    flex-direction: row;
    justify-content: space-between;
  }
  
  .action-button {
    flex: 1;
    max-width: 180px;
  }
}

.action-button {
  flex: 1;
  min-width: 120px;
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.primary-button {
  background: linear-gradient(135deg, #409EFF, #67C23A);
  border: none;
  color: white;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.primary-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(64, 158, 255, 0.4);
}

.secondary-button {
  background: #F5F7FA;
  border: 2px solid #E4E7ED;
  color: #606266;
}

.secondary-button:hover {
  background: #E4E7ED;
  border-color: #C0C4CC;
}

.info-button {
  background: #909399;
  border: none;
  color: white;
}

.info-button:hover {
  background: #82868A;
}

.card-header {
  text-align: center;
  color: #409EFF;
}

.card-header h2 {
  margin-bottom: 10px;
  font-size: 1.5rem;
}

.card-header p {
  margin: 0;
  font-size: 0.9rem;
}

.label-preview {
  text-align: center;
  border: 2px dashed #409EFF;
  padding: 20px;
  background-color: #f9f9f9;
  width: 100%;
  max-width: 58mm;
  margin: 0 auto;
  font-family: monospace;
}

.preview-header h3 {
  margin: 0;
  font-size: 14px;
  font-weight: bold;
}

.preview-content {
  text-align: left;
  font-size: 12px;
}

.qr-placeholder {
  text-align: center;
  border: 1px solid #ccc;
  padding: 20px;
  margin: 15px 0;
  background-color: white;
}

.qr-placeholder p {
  margin: 0;
  font-size: 24px;
}

.dialog-footer {
  width: 100%;
}

.actual-preview-container {
  text-align: center;
}

.preview-info {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 8px;
  border-left: 4px solid #409EFF;
}

.preview-info h3 {
  margin: 0 0 10px 0;
  color: #409EFF;
  font-size: 1.1rem;
}

.preview-info p {
  margin: 5px 0;
  color: #666;
  font-size: 0.9rem;
}

.actual-image-container {
  display: flex;
  justify-content: center;
  padding: 20px;
  background-color: #fafafa;
  border-radius: 8px;
  border: 2px dashed #409EFF;
}

.actual-preview-image {
  max-width: 100%;
  max-height: 500px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  background-color: white;
}

/* Mobile Responsiveness - Full Width */
@media (max-width: 768px) {
  .create-label-container {
    padding: 0px !important;
    margin: 0 !important;
    max-width: 100% !important;
    width: 100% !important;
  }
  
  .form-wrapper {
    width: 100% !important;
    margin: 0 !important;
    padding: 5px !important;
  }
  
  .card-header h2 {
    font-size: 1.3rem;
  }
  
  .card-header p {
    font-size: 0.8rem;
  }
  
  :deep(.el-card) {
    margin: 0 !important;
    border-radius: 8px;
    width: 100% !important;
    max-width: 100% !important;
  }
  
  .mobile-card {
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 !important;
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
    width: 90px !important;
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
  
  :deep(.el-input-group__append .el-button) {
    padding: 12px 15px;
    font-size: 14px;
  }
  
  :deep(.el-button) {
    font-size: 14px;
    padding: 12px 15px;
    box-sizing: border-box;
  }
  
  /* Button Group Mobile Layout */
  .button-group {
    flex-direction: column;
    gap: 8px;
  }
  
  .action-button {
    width: 100% !important;
    min-width: unset;
    margin-bottom: 8px;
    font-size: 14px;
    padding: 12px 16px;
    min-height: 44px;
  }
  
  .preview-info {
    padding: 12px;
  }
  
  .preview-info h3 {
    font-size: 1rem;
  }
  
  .preview-info p {
    font-size: 0.85rem;
  }
  
  .actual-image-container {
    padding: 15px;
  }
}

@media (max-width: 576px) {
  .create-label-container {
    padding: 3px;
  }
  
  /* Compact button layout for small screens */
  .button-group {
    gap: 6px;
  }
  
  .action-button {
    font-size: 13px;
    padding: 10px 12px;
    min-height: 42px;
  }
  
  .card-header h2 {
    font-size: 1.2rem;
  }
  
  .card-header p {
    font-size: 0.75rem;
  }
  
  :deep(.el-card__body) {
    padding: 12px;
  }
  
  :deep(.el-form-item__label) {
    font-size: 13px;
    margin-bottom: 5px;
    width: 80px !important;
  }
  
  :deep(.el-input__inner) {
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
  
  .label-preview {
    padding: 15px;
  }
  
  .qr-placeholder {
    padding: 15px;
    margin: 10px 0;
  }
  
  .qr-placeholder p {
    font-size: 20px;
  }
  
  .preview-info {
    padding: 10px;
  }
  
  .preview-info h3 {
    font-size: 0.9rem;
  }
  
  .preview-info p {
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .create-label-container {
    padding: 2px;
  }
  
  :deep(.el-card__body) {
    padding: 10px;
  }
  
  :deep(.el-form-item__label) {
    width: 70px !important;
    font-size: 12px;
  }
  
  :deep(.el-input-group__append .el-button) {
    padding: 8px 10px;
    font-size: 12px;
  }
  
  .dialog-footer :deep(.el-row) {
    margin: 0 -5px;
  }
  
  .dialog-footer :deep(.el-col) {
    padding: 0 5px;
    margin-bottom: 10px;
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
  .create-label-container {
    padding: 3px;
  }
  
  :deep(.el-card__body) {
    padding: 8px;
  }
  
  .card-header h2 {
    font-size: 1.1rem;
    margin-bottom: 5px;
  }
  
  .card-header p {
    font-size: 0.7rem;
  }
}
</style>