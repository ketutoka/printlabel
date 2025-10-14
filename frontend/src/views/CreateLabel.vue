<template>
  <div class="create-label-container">
    <el-row justify="center">
      <el-col :span="16">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <h2>🏷️ Buat Label Baru</h2>
              <p>Isi informasi untuk membuat label paket dengan QR Code</p>
            </div>
          </template>

          <el-form
            ref="labelFormRef"
            :model="labelForm"
            :rules="rules"
            label-width="120px"
            @submit.prevent="handleCreateLabel"
          >
            <el-form-item label="Nama Pengirim" prop="sender_name">
              <el-input
                v-model="labelForm.sender_name"
                placeholder="Masukkan nama pengirim"
                prefix-icon="User"
              />
            </el-form-item>

            <el-form-item label="Kode Pengiriman" prop="shipping_code">
              <el-input
                v-model="labelForm.shipping_code"
                placeholder="Masukkan kode pengiriman (contoh: PKG001)"
                prefix-icon="DocumentCopy"
              >
                <template #append>
                  <el-button @click="generateShippingCode">Generate</el-button>
                </template>
              </el-input>
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                :loading="labelStore.loading"
                @click="handleCreateLabel"
                size="large"
              >
                {{ labelStore.loading ? 'Membuat Label...' : 'Buat & Generate QR Code' }}
              </el-button>
              <el-button @click="resetForm" style="margin-left: 10px;">
                Reset
              </el-button>
              <el-button type="info" @click="$router.push('/dashboard')">
                Kembali
              </el-button>
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
      </el-col>
    </el-row>

    <!-- Preview Modal -->
    <el-dialog
      v-model="showPreview"
      title="Preview Label"
      width="400px"
      center
    >
      <div v-if="generatedLabel" class="label-preview">
        <div class="preview-header">
          <h3>🏷️ LABEL PENGIRIMAN</h3>
        </div>
        
        <el-divider />
        
        <div class="preview-content">
          <p><strong>Pengirim:</strong></p>
          <p>{{ generatedLabel.sender_name }}</p>
          
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
        <span class="dialog-footer">
          <el-button @click="showPreview = false">Tutup</el-button>
          <el-button 
            type="success" 
            @click="previewActualLabel"
          >
            👁️ Preview Asli
          </el-button>
          <el-button type="primary" @click="printLabel">
            🖨️ Print Label
          </el-button>
          <el-button type="info" @click="createAnotherLabel">
            Buat Label Lagi
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- Actual Label Preview Dialog -->
    <el-dialog
      v-model="showActualPreview"
      title="Preview Label Asli"
      width="600px"
      center
    >
      <div v-if="generatedLabel" class="actual-preview-container">
        <div class="preview-info">
          <h3>🏷️ {{ generatedLabel.shipping_code }}</h3>
          <p><strong>Pengirim:</strong> {{ generatedLabel.sender_name }}</p>
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
        <span class="dialog-footer">
          <el-button @click="showActualPreview = false">Tutup</el-button>
          <el-button type="primary" @click="printFromPreview">
            🖨️ Print Label Ini
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useLabelStore } from '../stores/label'
import { useUserStore } from '../stores/user'

const router = useRouter()
const labelStore = useLabelStore()
const userStore = useUserStore()

const labelFormRef = ref()
const showPreview = ref(false)
const showActualPreview = ref(false)
const generatedLabel = ref(null)
const actualPreviewUrl = ref('')

const labelForm = reactive({
  sender_name: '',
  shipping_code: ''
})

const rules = {
  sender_name: [
    { required: true, message: 'Nama pengirim harus diisi', trigger: 'blur' },
    { min: 2, message: 'Nama pengirim minimal 2 karakter', trigger: 'blur' }
  ],
  shipping_code: [
    { required: true, message: 'Kode pengiriman harus diisi', trigger: 'blur' },
    { min: 3, message: 'Kode pengiriman minimal 3 karakter', trigger: 'blur' },
    { max: 20, message: 'Kode pengiriman maksimal 20 karakter', trigger: 'blur' }
  ]
}

const generateShippingCode = () => {
  const timestamp = Date.now().toString().slice(-6)
  labelForm.shipping_code = `PKG${timestamp}`
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
  labelForm.sender_name = ''
  labelForm.shipping_code = ''
  labelStore.clearError()
}

const printLabel = async () => {
  try {
    // In real implementation, this would send to thermal printer
    // For now, we'll simulate printing
    ElMessage.success(`Label ${generatedLabel.value.shipping_code} berhasil dicetak!`)
    showPreview.value = false
    
    // Redirect to dashboard after successful print
    setTimeout(() => {
      router.push('/dashboard')
    }, 1000)
  } catch (error) {
    ElMessage.error('Gagal mencetak label')
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
      actualPreviewUrl.value = await labelStore.getPreviewUrl(generatedLabel.value.id)
      actualPreviewUrl.value += `?t=${Date.now()}` // Cache busting
      showActualPreview.value = true
      ElMessage.success('Menampilkan preview label asli')
    }
  } catch (error) {
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
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  text-align: center;
  color: #409EFF;
}

.card-header h2 {
  margin-bottom: 10px;
}

.label-preview {
  text-align: center;
  border: 2px dashed #409EFF;
  padding: 20px;
  background-color: #f9f9f9;
  width: 58mm; /* Thermal printer width */
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
  display: flex;
  justify-content: space-between;
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
}

.preview-info p {
  margin: 5px 0;
  color: #666;
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
</style>