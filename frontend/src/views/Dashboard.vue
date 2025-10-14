<template>
  <div class="dashboard-container">
    <el-row :gutter="20">
      <!-- Welcome Card -->
      <el-col :span="24">
        <el-card shadow="hover" style="margin-bottom: 20px;">
          <div class="welcome-section">
            <h2>🏷️ Selamat Datang di Print Label App</h2>
            <p>Aplikasi untuk mencetak label paket dengan QR Code untuk thermal printer 58mm</p>
          </div>
        </el-card>
      </el-col>

      <!-- Quick Actions -->
      <el-col :span="12">
        <el-card shadow="hover" class="action-card">
          <template #header>
            <div class="card-header">
              <span>📝 Buat Label Baru</span>
            </div>
          </template>
          <div class="card-content">
            <p>Buat dan cetak label paket dengan QR Code</p>
            <el-button 
              type="primary" 
              size="large"
              @click="$router.push('/create-label')"
              style="width: 100%; margin-top: 15px;"
            >
              Buat Label
            </el-button>
          </div>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card shadow="hover" class="action-card">
          <template #header>
            <div class="card-header">
              <span>📋 Riwayat Label</span>
            </div>
          </template>
          <div class="card-content">
            <p>Lihat dan cetak ulang label yang sudah dibuat</p>
            <el-button 
              type="success" 
              size="large"
              @click="showHistory = true"
              style="width: 100%; margin-top: 15px;"
            >
              Lihat Riwayat
            </el-button>
          </div>
        </el-card>
      </el-col>

      <!-- Recent Labels -->
      <el-col :span="24" style="margin-top: 20px;">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>🕒 Label Terbaru</span>
            </div>
          </template>
          
          <div v-if="labelStore.labels.length === 0" class="empty-state">
            <el-empty description="Belum ada label yang dibuat">
              <el-button type="primary" @click="$router.push('/create-label')">
                Buat Label Pertama
              </el-button>
            </el-empty>
          </div>

          <el-table v-else :data="recentLabels" stripe>
            <el-table-column prop="shipping_code" label="Kode Pengiriman" width="180" />
            <el-table-column prop="sender_name" label="Pengirim" />
            <el-table-column prop="created_at" label="Tanggal Dibuat" width="180">
              <template #default="scope">
                {{ formatDate(scope.row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="Aksi" width="180">
              <template #default="scope">
                <el-button 
                  type="success" 
                  size="small"
                  @click="previewLabel(scope.row)"
                  style="margin-right: 5px;"
                >
                  👁️ Preview
                </el-button>
                <el-button 
                  type="primary" 
                  size="small"
                  @click="printLabel(scope.row)"
                >
                  🖨️ Print
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- Statistics Cards -->
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="8">
        <el-card shadow="hover" class="stat-card">
          <el-statistic 
            title="Total Label" 
            :value="labelStore.labels.length"
            prefix="🏷️"
          />
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card shadow="hover" class="stat-card">
          <el-statistic 
            title="Label Hari Ini" 
            :value="todayLabelsCount"
            prefix="📅"
          />
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card shadow="hover" class="stat-card">
          <el-statistic 
            title="Label Minggu Ini" 
            :value="weekLabelsCount"
            prefix="📊"
          />
        </el-card>
      </el-col>
    </el-row>

    <!-- Label Preview Dialog -->
    <el-dialog
      v-model="showLabelPreview"
      title="Preview Label"
      width="500px"
      center
    >
      <div v-if="previewLabelData" class="preview-container">
        <div class="label-info">
          <h3>📦 {{ previewLabelData.shipping_code }}</h3>
          <p><strong>Pengirim:</strong> {{ previewLabelData.sender_name }}</p>
          <p><strong>Tanggal:</strong> {{ formatDate(previewLabelData.created_at) }}</p>
        </div>
        
        <div class="label-image-container">
          <img 
            :src="previewImageUrl" 
            alt="Label Preview"
            class="label-preview-image"
            @error="handleImageError"
          />
        </div>
      </div>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showLabelPreview = false">Tutup</el-button>
          <el-button 
            type="primary" 
            @click="printLabel(previewLabelData)"
          >
            🖨️ Print Label Ini
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useLabelStore } from '../stores/label'
import { useUserStore } from '../stores/user'

const labelStore = useLabelStore()
const userStore = useUserStore()

// Preview state
const showLabelPreview = ref(false)
const previewLabelData = ref(null)
const previewImageUrl = ref('')

const recentLabels = computed(() => 
  labelStore.labels.slice(0, 5) // Show only last 5 labels
)

const todayLabelsCount = computed(() => {
  const today = new Date().toDateString()
  return labelStore.labels.filter(label => 
    new Date(label.created_at).toDateString() === today
  ).length
})

const weekLabelsCount = computed(() => {
  const weekAgo = new Date()
  weekAgo.setDate(weekAgo.getDate() - 7)
  return labelStore.labels.filter(label => 
    new Date(label.created_at) > weekAgo
  ).length
})

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('id-ID', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const printLabel = async (label) => {
  try {
    const result = await labelStore.getLabelForPrint(label.id)
    if (result.success) {
      // Here you would implement actual printing
      // For now, we'll just show success message
      ElMessage.success(`Label ${label.shipping_code} siap dicetak!`)
      
      // In a real app, you might:
      // - Open print dialog
      // - Send to thermal printer
      // - Download as image/PDF
      console.log('Print data:', result.data)
    }
  } catch (error) {
    ElMessage.error('Gagal memuat data label untuk print')
  }
}

const previewLabel = async (label) => {
  try {
    previewLabelData.value = label
    previewImageUrl.value = await labelStore.getPreviewUrl(label.id)
    
    // Add authorization header to the image URL
    const token = userStore.token
    if (token) {
      previewImageUrl.value += `?t=${Date.now()}` // Cache busting
    }
    
    showLabelPreview.value = true
    ElMessage.success(`Preview label ${label.shipping_code}`)
  } catch (error) {
    ElMessage.error('Gagal memuat preview label')
  }
}

const handleImageError = () => {
  ElMessage.error('Gagal memuat gambar label')
}

onMounted(() => {
  // Load user data if not already loaded
  if (!userStore.user && userStore.token) {
    userStore.getCurrentUser()
  }
})
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-section {
  text-align: center;
  padding: 20px;
}

.welcome-section h2 {
  color: #409EFF;
  margin-bottom: 10px;
}

.action-card {
  height: 200px;
}

.card-header {
  font-weight: bold;
  color: #409EFF;
}

.card-content {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 120px;
}

.stat-card {
  text-align: center;
}

.empty-state {
  padding: 40px;
  text-align: center;
}

.preview-container {
  text-align: center;
}

.label-info {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.label-info h3 {
  margin: 0 0 10px 0;
  color: #409EFF;
}

.label-info p {
  margin: 5px 0;
  color: #666;
}

.label-image-container {
  display: flex;
  justify-content: center;
  padding: 20px;
  background-color: #fafafa;
  border-radius: 8px;
  border: 2px dashed #ddd;
}

.label-preview-image {
  max-width: 100%;
  max-height: 400px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.dialog-footer {
  display: flex;
  justify-content: space-between;
  width: 100%;
}
</style>