<template>
  <div class="qr-scanner-container">
    <!-- Scanner Modal -->
    <el-dialog
      v-model="showScanner"
      title="Scan QR Code / Barcode"
      :width="dialogWidth"
      :fullscreen="isMobile"
      @close="stopScanning"
      center
    >
      <div class="scanner-content">
        <div class="scanner-info">
          <el-alert
            title="Arahkan kamera ke QR Code atau Barcode"
            type="info"
            :closable="false"
            show-icon
          />
        </div>

        <!-- Camera Scanner -->
        <div class="scanner-wrapper">
          <div id="qr-reader" class="qr-reader"></div>
        </div>

        <!-- Manual Input Alternative -->
        <el-divider>Atau masukkan manual</el-divider>
        
        <el-input
          v-model="manualCode"
          placeholder="Ketik kode resi secara manual..."
          clearable
          @keyup.enter="handleManualInput"
        >
          <template #append>
            <el-button 
              type="primary" 
              @click="handleManualInput"
              :disabled="!manualCode.trim()"
            >
              OK
            </el-button>
          </template>
        </el-input>
      </div>

      <template #footer>
        <div class="scanner-footer">
          <el-row :gutter="10">
            <el-col :xs="12" :sm="8">
              <el-button @click="stopScanning" style="width: 100%;">Batal</el-button>
            </el-col>
            <el-col :xs="12" :sm="8" v-if="cameras.length > 1">
              <el-button type="info" @click="switchCamera" style="width: 100%;">
                📷 Ganti Kamera
              </el-button>
            </el-col>
          </el-row>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Html5QrcodeScanner, Html5Qrcode } from 'html5-qrcode'

// Props and Emits
const emit = defineEmits(['scan-success', 'scan-error'])

// Reactive variables
const showScanner = ref(false)
const manualCode = ref('')
const scanner = ref(null)
const cameras = ref([])
const currentCameraIndex = ref(0)

// Responsive design computed properties
const isMobile = computed(() => {
  return window.innerWidth < 768
})

const dialogWidth = computed(() => {
  if (window.innerWidth < 576) return '95%'
  if (window.innerWidth < 768) return '90%'
  return '500px'
})

// Start scanning function
const startScanning = async () => {
  try {
    showScanner.value = true
    
    // Wait for dialog to render
    await new Promise(resolve => setTimeout(resolve, 100))
    
    // Get available cameras
    const devices = await Html5Qrcode.getCameras()
    cameras.value = devices
    
    if (devices.length === 0) {
      throw new Error('Tidak ada kamera yang tersedia')
    }

    // Initialize scanner
    scanner.value = new Html5QrcodeScanner(
      "qr-reader",
      {
        fps: 10,
        qrbox: { width: 250, height: 250 },
        aspectRatio: 1.0
      }
    )

    // Start scanning
    scanner.value.render(onScanSuccess, onScanFailure)
    
    ElMessage.success('Scanner siap! Arahkan kamera ke QR Code atau Barcode')
    
  } catch (error) {
    console.error('Scanner error:', error)
    ElMessage.error('Gagal memulai scanner: ' + error.message)
    emit('scan-error', error.message)
  }
}

// Stop scanning function
const stopScanning = () => {
  try {
    if (scanner.value) {
      scanner.value.clear()
      scanner.value = null
    }
    showScanner.value = false
    manualCode.value = ''
  } catch (error) {
    console.error('Error stopping scanner:', error)
  }
}

// Handle successful scan
const onScanSuccess = (decodedText) => {
  try {
    // Clean and validate the scanned text
    const cleanedCode = decodedText.trim()
    
    if (cleanedCode) {
      ElMessage.success(`Berhasil scan: ${cleanedCode}`)
      emit('scan-success', cleanedCode)
      stopScanning()
    } else {
      ElMessage.warning('Kode yang discan kosong')
    }
  } catch (error) {
    console.error('Scan success handler error:', error)
    ElMessage.error('Gagal memproses hasil scan')
  }
}

// Handle scan failure
const onScanFailure = (error) => {
  // Don't show error for every failed scan attempt
  // Only log to console for debugging
  console.debug('Scan attempt failed:', error)
}

// Handle manual input
const handleManualInput = () => {
  const code = manualCode.value.trim()
  if (code) {
    ElMessage.success(`Kode manual: ${code}`)
    emit('scan-success', code)
    stopScanning()
  } else {
    ElMessage.warning('Masukkan kode terlebih dahulu')
  }
}

// Switch camera (if multiple cameras available)
const switchCamera = async () => {
  try {
    if (cameras.value.length <= 1) return
    
    // Stop current scanner
    if (scanner.value) {
      scanner.value.clear()
    }
    
    // Switch to next camera
    currentCameraIndex.value = (currentCameraIndex.value + 1) % cameras.value.length
    
    // Restart scanner with new camera
    await new Promise(resolve => setTimeout(resolve, 500))
    
    scanner.value = new Html5QrcodeScanner(
      "qr-reader",
      {
        fps: 10,
        qrbox: { width: 250, height: 250 },
        aspectRatio: 1.0,
        preferredCamera: cameras.value[currentCameraIndex.value].id
      }
    )
    
    scanner.value.render(onScanSuccess, onScanFailure)
    
    ElMessage.info(`Beralih ke kamera ${currentCameraIndex.value + 1}`)
    
  } catch (error) {
    console.error('Camera switch error:', error)
    ElMessage.error('Gagal mengganti kamera')
  }
}

// Cleanup on component unmount
onUnmounted(() => {
  stopScanning()
})

// Expose methods to parent component
defineExpose({
  startScanning,
  stopScanning
})
</script>

<style scoped>
.qr-scanner-container {
  display: inline-block;
}

.scanner-content {
  text-align: center;
}

.scanner-info {
  margin-bottom: 20px;
}

.scanner-wrapper {
  position: relative;
  margin: 20px auto;
  max-width: 400px;
}

.qr-reader {
  border: 2px dashed #409EFF;
  border-radius: 8px;
  overflow: hidden;
}

.scanner-footer {
  width: 100%;
}

/* Override html5-qrcode styles */
:deep(#qr-reader) {
  border: 2px dashed #409EFF !important;
}

:deep(#qr-reader__dashboard) {
  padding: 10px !important;
}

:deep(#qr-reader__camera_selection) {
  margin: 10px 0 !important;
}

:deep(#qr-reader__scan_region) {
  margin: 10px auto !important;
}

:deep(.qr-code-text) {
  font-size: 12px !important;
  color: #666 !important;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .scanner-wrapper {
    max-width: 100%;
  }
  
  .scanner-content {
    padding: 0 10px;
  }
  
  .scanner-info {
    margin-bottom: 15px;
  }
  
  :deep(#qr-reader) {
    width: 100% !important;
  }
  
  :deep(.qr-code-text) {
    font-size: 11px !important;
  }
}

@media (max-width: 576px) {
  .scanner-content {
    padding: 0 5px;
  }
  
  .scanner-info {
    margin-bottom: 10px;
  }
  
  :deep(#qr-reader__dashboard) {
    padding: 5px !important;
  }
  
  :deep(.qr-code-text) {
    font-size: 10px !important;
  }
}
</style>