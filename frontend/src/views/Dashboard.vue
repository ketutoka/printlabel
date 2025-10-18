<template>
  <div class="dashboard-container">
    <!-- User Header with Profile Dropdown -->
    <el-row style="margin-bottom: 20px;">
      <el-col :span="24">
        <el-card shadow="never" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
          <div class="user-header">
            <div class="user-info">
              <p>Aplikasi cetak label thermal printer 58mm</p>
            </div>
            <div class="user-profile">
              <el-dropdown @command="handleCommand" placement="bottom-end">
                <div class="profile-trigger">
                  <el-avatar 
                    :size="40" 
                    style="background-color: rgba(255,255,255,0.2); color: white; cursor: pointer;"
                  >
                    <el-icon><User /></el-icon>
                  </el-avatar>
                  <span class="username">{{ userStore.user?.name || 'User' }}</span>
                  <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
                </div>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item disabled style="color: #909399; font-size: 12px;">
                      {{ userStore.user?.email }}
                    </el-dropdown-item>
                    <el-dropdown-item divided command="profile">
                      <el-icon><Setting /></el-icon>
                      Edit Profil
                    </el-dropdown-item>
                    <el-dropdown-item command="logout" style="color: #F56C6C;">
                      <el-icon><SwitchButton /></el-icon>
                      Logout
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
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

      <!-- Quick Actions - Responsive Grid -->
      <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
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

      <el-col :xs="24" :sm="12" :md="12" :lg="12" :xl="12">
        <el-card shadow="hover" class="action-card">
          <template #header>
            <div class="card-header">
              <span>📦 Label Pengiriman</span>
            </div>
          </template>
          <div class="card-content">
            <p>Buat label pengiriman lengkap dengan alamat</p>
            <el-button 
              type="warning" 
              size="large"
              @click="$router.push('/create-shipping-label')"
              style="width: 100%; margin-top: 15px;"
            >
              Buat Label Kirim
            </el-button>
          </div>
        </el-card>
      </el-col>

      <!-- Recent Labels with Search and Pagination -->
      <el-col :span="24" style="margin-top: 20px;">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>� Riwayat Label</span>
              <div class="header-actions">
                <el-input
                  v-model="searchQuery"
                  placeholder="Cari berdasarkan detail..."
                  style="width: 250px; margin-right: 10px;"
                  clearable
                  @input="handleSearch"
                >
                  <template #prefix>
                    <el-icon><Search /></el-icon>
                  </template>
                </el-input>
                <el-button 
                  type="primary" 
                  size="small" 
                  @click="refreshLabels"
                  :loading="labelStore.loading"
                >
                  🔄 Refresh
                </el-button>
              </div>
            </div>
          </template>
          
          <div v-if="(labelStore.loading || shippingStore.loading) && filteredLabels.length === 0" class="loading-state">
            <el-icon class="is-loading"><Loading /></el-icon>
            <p>Memuat daftar label...</p>
          </div>
          
          <div v-else-if="filteredLabels.length === 0" class="empty-state">
            <el-empty description="Belum ada label yang dibuat">
              <el-button type="primary" @click="$router.push('/create-label')">
                Buat Label Pertama
              </el-button>
            </el-empty>
          </div>

          <div v-else>
            <!-- Bulk Actions Bar -->
            <div v-if="selectedLabels.length > 0" class="bulk-actions-bar">
              <el-alert
                :title="`${selectedLabels.length} label dipilih`"
                type="info"
                :closable="false"
                show-icon
              >
                <template #default>
                  <div class="bulk-actions">
                    <el-button 
                      type="danger" 
                      size="small" 
                      @click="bulkDeleteLabels"
                      :loading="labelStore.loading || shippingStore.loading"
                    >
                      <el-icon><Delete /></el-icon>
                      Hapus Terpilih ({{ selectedLabels.length }})
                    </el-button>
                    <el-button 
                      size="small" 
                      @click="clearSelection"
                    >
                      Batal Pilihan
                    </el-button>
                  </div>
                </template>
              </el-alert>
            </div>

            <el-table 
              :data="paginatedLabels" 
              stripe 
              @selection-change="handleSelectionChange"
            >
              <el-table-column type="selection" width="55" />
              <el-table-column label="Aksi" width="80" fixed="left">
                <template #default="scope">
                  <el-dropdown @command="(command) => handleActionCommand(command, scope.row)" placement="bottom-start">
                    <el-button 
                      type="primary" 
                      size="small"
                      :title="'Menu Aksi'"
                    >
                      <el-icon><ArrowDown /></el-icon>
                    </el-button>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item command="preview">
                          <el-icon><View /></el-icon>
                          Preview Label
                        </el-dropdown-item>
                        <el-dropdown-item command="print">
                          <el-icon><Printer /></el-icon>
                          Print Label
                        </el-dropdown-item>
                        <el-dropdown-item command="delete" style="color: #F56C6C;" divided>
                          <el-icon><Delete /></el-icon>
                          Hapus Label
                        </el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </template>
              </el-table-column>
              <el-table-column prop="type" label="Jenis" width="100">
                <template #default="scope">
                  <el-tag :type="scope.row.type === 'simple' ? 'success' : 'warning'">
                    {{ scope.row.type === 'simple' ? '📝 Sederhana' : '📦 Kirim' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="shipping_code" label="Kode/Resi" width="180" />
              <el-table-column prop="display_name" label="Detail" />
              <el-table-column prop="created_at" label="Tanggal Dibuat" width="180">
                <template #default="scope">
                  {{ formatDate(scope.row.created_at) }}
                </template>
              </el-table-column>
            </el-table>
            
            <!-- Pagination -->
            <div class="pagination-container">
              <el-pagination
                v-model:current-page="currentPage"
                v-model:page-size="pageSize"
                :page-sizes="[5, 10, 20, 50]"
                :total="filteredLabels.length"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
              />
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Statistics Cards -->
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="8">
        <el-card shadow="hover" class="stat-card">
          <el-statistic 
            title="Total Label" 
            :value="totalLabelsCount"
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
      :width="dialogWidth"
      :fullscreen="isMobilePreview"
      center
    >
      <div v-if="previewLabelData" class="preview-container">
        <div class="label-info">
          <h3>📦 {{ previewLabelData.shipping_code }}</h3>
          <p><strong>Pengirim:</strong> {{ previewLabelData.sender_name }}</p>
          <p><strong>Tanggal:</strong> {{ formatDate(previewLabelData.created_at) }}</p>
        </div>
        
        <div class="label-image-container">
          <div v-if="!previewImageUrl" class="loading-placeholder">
            <el-icon class="is-loading"><Loading /></el-icon>
            <p>Memuat preview...</p>
          </div>
          <img 
            v-else
            :src="previewImageUrl" 
            alt="Label Preview"
            class="label-preview-image"
            @error="handleImageError"
          />
        </div>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showLabelPreview = false" size="large">Tutup</el-button>
          <el-button 
            type="primary" 
            @click="printLabel(previewLabelData)"
            size="large"
          >
            🖨️ Print Label Ini
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, Setting, SwitchButton, ArrowDown, View, Printer, Search, Delete, Loading } from '@element-plus/icons-vue'
import { useLabelStore } from '../stores/label'
import { useShippingStore } from '../stores/shipping'
import { useUserStore } from '../stores/user'
import api from '../services/api'

const router = useRouter()

const labelStore = useLabelStore()
const shippingStore = useShippingStore()
const userStore = useUserStore()

// Preview state
const showLabelPreview = ref(false)
const previewLabelData = ref(null)
const previewImageUrl = ref('')

// Search and pagination state
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(10)

// Selection state for bulk operations
const selectedLabels = ref([])
const isAllSelected = ref(false)

const recentLabels = computed(() => {
  // Gabungkan simple labels dan shipping labels
  const simpleLabels = labelStore.labels.map(label => ({
    ...label,
    type: 'simple',
    display_name: label.sender_name || 'Label Sederhana',
    shipping_code: label.shipping_code || '-'
  }))
  
  const shippingLabels = shippingStore.shippingLabels.map(label => ({
    ...label,
    type: 'shipping',
    display_name: `${label.sender_name} → ${label.recipient_name}`,
    shipping_code: label.shipping_code || '(Tanpa Resi)'
  }))
  
  // Gabungkan dan urutkan berdasarkan tanggal terbaru
  const allLabels = [...simpleLabels, ...shippingLabels]
  return allLabels
    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
})

// Filtered labels based on search query
const filteredLabels = computed(() => {
  if (!searchQuery.value) {
    return recentLabels.value
  }
  
  return recentLabels.value.filter(label => {
    const searchTerm = searchQuery.value.toLowerCase()
    return (
      label.display_name.toLowerCase().includes(searchTerm) ||
      (label.shipping_code && label.shipping_code.toLowerCase().includes(searchTerm)) ||
      (label.sender_name && label.sender_name.toLowerCase().includes(searchTerm)) ||
      (label.recipient_name && label.recipient_name.toLowerCase().includes(searchTerm))
    )
  })
})

// Paginated labels
const paginatedLabels = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredLabels.value.slice(start, end)
})

const todayLabelsCount = computed(() => {
  const today = new Date().toDateString()
  const simpleToday = labelStore.labels.filter(label => 
    new Date(label.created_at).toDateString() === today
  ).length
  const shippingToday = shippingStore.shippingLabels.filter(label => 
    new Date(label.created_at).toDateString() === today
  ).length
  return simpleToday + shippingToday
})

const weekLabelsCount = computed(() => {
  const weekAgo = new Date()
  weekAgo.setDate(weekAgo.getDate() - 7)
  const simpleWeek = labelStore.labels.filter(label => 
    new Date(label.created_at) > weekAgo
  ).length
  const shippingWeek = shippingStore.shippingLabels.filter(label => 
    new Date(label.created_at) > weekAgo
  ).length
  return simpleWeek + shippingWeek
})

const totalLabelsCount = computed(() => {
  return labelStore.labels.length + shippingStore.shippingLabels.length
})

// Responsive dialog properties
const isMobilePreview = computed(() => {
  return window.innerWidth <= 768
})

const dialogWidth = computed(() => {
  if (window.innerWidth <= 480) return '95%'
  if (window.innerWidth <= 768) return '90%'
  if (window.innerWidth <= 992) return '80%'
  return '500px'
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

// Search and pagination handlers
const handleSearch = () => {
  currentPage.value = 1 // Reset to first page when searching
}

const handleSizeChange = (newSize) => {
  pageSize.value = newSize
  currentPage.value = 1
}

const handleCurrentChange = (newPage) => {
  currentPage.value = newPage
}

// Handle dropdown action commands
const handleActionCommand = (command, label) => {
  switch (command) {
    case 'preview':
      previewLabel(label)
      break
    case 'print':
      printLabel(label)
      break
    case 'delete':
      deleteLabel(label)
      break
    default:
      console.warn('Unknown command:', command)
  }
}

const printLabel = async (label) => {
  try {
    let result
    // Check label type and use appropriate store method
    if (label.type === 'shipping') {
      result = await shippingStore.getShippingLabelForPrint(label.id)
    } else {
      result = await labelStore.getLabelForPrint(label.id)
    }
    
    if (result.success) {
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
        printViaBrowser(label)
      }).catch((action) => {
        if (action === 'cancel') {
          // Download image
          downloadLabel(label)
        }
      })
    } else {
      ElMessage.error(result.error || 'Gagal memuat label untuk print')
    }
  } catch (error) {
    console.error('Error printing label:', error)
    ElMessage.error('Terjadi kesalahan saat mencetak label')
  }
}

const printViaBrowser = async (label) => {
  try {
    // Get the preview image URL based on label type
    const token = userStore.token
    let imageUrl
    if (label.type === 'shipping') {
      imageUrl = `${api.defaults.baseURL}/shipping-labels/preview/${label.id}?token=${token}`
    } else {
      imageUrl = `${api.defaults.baseURL}/labels/preview/${label.id}?token=${token}`
    }
    
    // Create a new window for printing
    const printWindow = window.open('', '_blank')
    const labelCode = label.shipping_code || 'Label'
    printWindow.document.write(`
      <!DOCTYPE html>
      <html>
      <head>
        <title>Print Label - ${labelCode}</title>
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
        <img src="${imageUrl}" alt="Label ${label.shipping_code}" onload="window.print(); window.close();" />
      </body>
      </html>
    `)
    printWindow.document.close()
    
    ElMessage.success(`Label ${label.shipping_code} dikirim ke printer!`)
  } catch (error) {
    ElMessage.error('Gagal mencetak label')
    console.error('Print error:', error)
  }
}

const downloadLabel = async (label) => {
  try {
    const token = userStore.token
    let imageUrl
    if (label.type === 'shipping') {
      imageUrl = `${api.defaults.baseURL}/shipping-labels/preview/${label.id}?token=${token}`
    } else {
      imageUrl = `${api.defaults.baseURL}/labels/preview/${label.id}?token=${token}`
    }
    
    // Create download link
    const link = document.createElement('a')
    link.href = imageUrl
    const labelCode = label.shipping_code || `label_${label.id}`
    link.download = `${labelCode}.png`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    ElMessage.success(`Label ${labelCode} berhasil didownload!`)
  } catch (error) {
    ElMessage.error('Gagal download label')
    console.error('Download error:', error)
  }
}

const previewLabel = async (label) => {
  try {
    previewLabelData.value = label
    previewImageUrl.value = '' // Reset image URL to show loading
    showLabelPreview.value = true
    
    ElMessage.info('Memuat preview label...')
    
    // Get preview URL based on label type
    if (label.type === 'shipping') {
      previewImageUrl.value = await shippingStore.getPreviewUrl(label.id)
    } else {
      previewImageUrl.value = await labelStore.getPreviewUrl(label.id)
    }
    
    const labelCode = label.shipping_code || 'Label'
    ElMessage.success(`Preview label ${labelCode} berhasil dimuat`)
  } catch (error) {
    console.error('Preview error:', error)
    ElMessage.error('Gagal memuat preview label')
    showLabelPreview.value = false
  }
}

const handleImageError = () => {
  ElMessage.error('Gagal memuat gambar label')
}

const refreshLabels = async () => {
  try {
    // Fetch both simple labels and shipping labels
    const simpleResult = await labelStore.fetchLabels()
    const shippingResult = await shippingStore.fetchShippingLabels()
    
    if (simpleResult.success && shippingResult.success) {
      ElMessage.success('Daftar label berhasil diperbarui')
    } else {
      ElMessage.error('Gagal memperbarui daftar label')
    }
  } catch (error) {
    ElMessage.error('Gagal memperbarui daftar label')
  }
}

onMounted(() => {
  // Load user data if not already loaded
  if (!userStore.user && userStore.token) {
    userStore.getCurrentUser()
  }
  
  // Load both types of labels if user is authenticated
  if (userStore.isAuthenticated) {
    if (labelStore.labels.length === 0) {
      labelStore.fetchLabels()
    }
    if (shippingStore.shippingLabels.length === 0) {
      shippingStore.fetchShippingLabels()
    }
  }
})

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm(
      'Apakah Anda yakin ingin logout?',
      'Konfirmasi Logout',
      {
        confirmButtonText: 'Ya, Logout',
        cancelButtonText: 'Batal',
        type: 'warning',
      }
    )
    
    userStore.logout()
    ElMessage.success('Berhasil logout!')
  } catch {
    // User cancelled logout
  }
}

const deleteLabel = async (label) => {
  try {
    const labelCode = label.shipping_code || `Label #${label.id}`
    
    await ElMessageBox.confirm(
      `Apakah Anda yakin ingin menghapus "${labelCode}"? Tindakan ini tidak dapat dibatalkan.`,
      'Konfirmasi Hapus Label',
      {
        confirmButtonText: 'Ya, Hapus',
        cancelButtonText: 'Batal',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )
    
    let result
    
    // Delete based on label type
    if (label.type === 'shipping') {
      result = await shippingStore.deleteShippingLabel(label.id)
    } else {
      result = await labelStore.deleteLabel(label.id)
    }
    
    if (result.success) {
      ElMessage.success(`Label "${labelCode}" berhasil dihapus!`)
      // Clear selection if deleted item was selected
      selectedLabels.value = selectedLabels.value.filter(selected => selected.id !== label.id)
    } else {
      ElMessage.error(result.error || 'Gagal menghapus label')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Error deleting label:', error)
      ElMessage.error('Terjadi kesalahan saat menghapus label')
    }
    // If error is 'cancel', user cancelled the action, so do nothing
  }
}

const bulkDeleteLabels = async () => {
  try {
    if (selectedLabels.value.length === 0) {
      ElMessage.warning('Belum ada label yang dipilih')
      return
    }
    
    const labelCount = selectedLabels.value.length
    const labelText = labelCount === 1 ? 'label' : 'label'
    
    await ElMessageBox.confirm(
      `Apakah Anda yakin ingin menghapus ${labelCount} ${labelText} terpilih? Tindakan ini tidak dapat dibatalkan.`,
      'Konfirmasi Hapus Massal',
      {
        confirmButtonText: 'Ya, Hapus Semua',
        cancelButtonText: 'Batal',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )
    
    // Separate labels by type for bulk operations
    const simpleLabels = selectedLabels.value.filter(label => label.type === 'simple')
    const shippingLabels = selectedLabels.value.filter(label => label.type === 'shipping')
    
    let totalSuccess = 0
    let totalErrors = 0
    const allErrors = []
    
    // Bulk delete simple labels
    if (simpleLabels.length > 0) {
      const simpleIds = simpleLabels.map(label => label.id)
      const result = await labelStore.bulkDeleteLabels(simpleIds)
      
      if (result.success) {
        totalSuccess += result.results.deleted_count
        totalErrors += result.results.failed_count
        if (result.results.errors.length > 0) {
          allErrors.push(...result.results.errors)
        }
      } else {
        totalErrors += simpleLabels.length
        allErrors.push(`Simple labels: ${result.error}`)
      }
    }
    
    // Bulk delete shipping labels  
    if (shippingLabels.length > 0) {
      const shippingIds = shippingLabels.map(label => label.id)
      const result = await shippingStore.bulkDeleteShippingLabels(shippingIds)
      
      if (result.success) {
        totalSuccess += result.results.deleted_count
        totalErrors += result.results.failed_count
        if (result.results.errors.length > 0) {
          allErrors.push(...result.results.errors)
        }
      } else {
        totalErrors += shippingLabels.length
        allErrors.push(`Shipping labels: ${result.error}`)
      }
    }
    
    // Clear selection after deletion attempt
    selectedLabels.value = []
    
    // Show results
    if (totalSuccess === labelCount) {
      ElMessage.success(`${totalSuccess} label berhasil dihapus!`)
    } else if (totalSuccess > 0) {
      ElMessage.warning(`${totalSuccess} label berhasil dihapus, ${totalErrors} label gagal dihapus`)
      if (allErrors.length > 0) {
        console.error('Delete errors:', allErrors)
      }
    } else {
      ElMessage.error(`Gagal menghapus semua label. Error: ${allErrors.slice(0, 3).join(', ')}${allErrors.length > 3 ? '...' : ''}`)
    }
    
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Error bulk deleting labels:', error)
      ElMessage.error('Terjadi kesalahan saat menghapus label')
    }
  }
}

const handleSelectionChange = (selection) => {
  selectedLabels.value = selection
}

const clearSelection = () => {
  selectedLabels.value = []
}

const handleCommand = (command) => {
  switch (command) {
    case 'profile':
      router.push('/profile/edit')
      break
    case 'logout':
      handleLogout()
      break
  }
}
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 10px;
}

.user-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
}

.user-info h3 {
  margin: 0 0 5px 0;
  font-size: 20px;
}

.user-info p {
  margin: 0;
  opacity: 0.9;
  font-size: 14px;
}

.user-profile {
  display: flex;
  align-items: center;
}

.profile-trigger {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 20px;
  transition: background-color 0.3s;
}

.profile-trigger:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.username {
  font-weight: 500;
  font-size: 14px;
}

.dropdown-icon {
  font-size: 12px;
  transition: transform 0.3s;
}

/* Action button with arrow down styling */
.el-table .el-dropdown .el-button {
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 14px;
  min-width: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.el-table .el-dropdown .el-button .el-icon {
  font-size: 16px;
  transition: transform 0.2s ease;
}

.el-table .el-dropdown:hover .el-button .el-icon {
  transform: rotate(180deg);
}

.el-table .el-dropdown .el-button:hover {
  background-color: #337ecc;
  border-color: #337ecc;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .dashboard-container {
    padding: 5px;
    margin: 0;
    max-width: 100%;
  }
  
  /* Mobile dialog optimization */
  :deep(.el-dialog) {
    margin: 5px !important;
    max-height: calc(100vh - 10px) !important;
    width: calc(100vw - 10px) !important;
  }
  
  :deep(.el-dialog__body) {
    padding: 10px !important;
    max-height: calc(100vh - 150px) !important;
    overflow-y: auto !important;
  }
  
  :deep(.el-dialog__header) {
    padding: 15px !important;
  }
  
  :deep(.el-dialog__footer) {
    padding: 10px !important;
  }
  
  .user-info h3 {
    font-size: 16px;
  }
  
  .user-info p {
    font-size: 12px;
  }
  
  .username {
    display: none; /* Hide username on mobile to save space */
  }
  
  .user-header {
    padding: 8px 0;
  }
  
  .card-header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
  
  .header-actions {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .header-actions .el-input {
    width: 100% !important;
  }
  
  .action-card {
    height: auto;
    margin-bottom: 15px;
  }
  
  .card-content {
    height: auto;
  }
  
  :deep(.el-table .el-table-column.is-left .cell) {
    font-size: 12px;
  }
  
  .pagination-container {
    overflow-x: auto;
  }
  
  .pagination-container .el-pagination {
    justify-content: center;
    flex-wrap: wrap;
  }
  
  :deep(.el-table__body-wrapper) {
    overflow-x: auto;
  }
  
  :deep(.el-card) {
    margin: 0;
    border-radius: 8px;
  }
  
  :deep(.el-card__body) {
    padding: 12px;
  }
  
  /* Mobile action button optimization */
  .el-table .el-dropdown .el-button {
    padding: 6px 10px;
    min-width: 40px;
    font-size: 12px;
  }
  
  .el-table .el-dropdown .el-button .el-icon {
    font-size: 14px;
  }
  
  /* Mobile preview optimization */
  .preview-container {
    padding: 0;
    margin: 0;
  }
  
  .label-info {
    margin-bottom: 15px;
    padding: 12px;
    font-size: 14px;
  }
  
  .label-info h3 {
    font-size: 1rem;
    line-height: 1.2;
  }
  
  .label-info p {
    font-size: 0.85rem;
    line-height: 1.3;
  }
  
  .label-image-container {
    padding: 10px;
    margin: 0;
  }
  
  .label-preview-image {
    max-height: 300px;
    width: 100%;
    height: auto;
  }
  
  .dialog-footer {
    flex-direction: column;
    gap: 10px;
  }
  
  .dialog-footer .el-button {
    width: 100%;
    margin: 0;
  }
}

@media (max-width: 480px) {
  .dashboard-container {
    padding: 3px;
  }
  
  .user-info h3 {
    font-size: 14px;
  }
  
  .user-info p {
    font-size: 11px;
  }
  
  .header-actions {
    align-items: stretch;
  }
  
  .bulk-actions {
    flex-direction: column;
    align-items: stretch;
    gap: 5px;
  }
  
  .bulk-actions .el-button {
    width: 100%;
    margin: 2px 0;
  }
  
  :deep(.el-table) {
    font-size: 12px;
  }
  
  :deep(.el-table .cell) {
    padding: 5px;
  }
  
  :deep(.el-button--small) {
    padding: 6px 10px;
    font-size: 11px;
  }
  
  .welcome-section h2 {
    font-size: 1.2rem;
  }
  
  .welcome-section p {
    font-size: 0.85rem;
  }
  
  :deep(.el-card__body) {
    padding: 10px;
  }
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
  display: flex;
  justify-content: space-between;
  align-items: center;
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
  width: 100%;
  overflow-x: hidden;
}

.label-info {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 8px;
  width: 100%;
  box-sizing: border-box;
}

.label-info h3 {
  margin: 0 0 10px 0;
  color: #409EFF;
  font-size: 1.1rem;
  word-wrap: break-word;
}

.label-info p {
  margin: 5px 0;
  color: #666;
  font-size: 0.9rem;
  word-wrap: break-word;
}

.label-image-container {
  display: flex;
  justify-content: center;
  padding: 20px;
  background-color: #fafafa;
  border-radius: 8px;
  border: 2px dashed #ddd;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

.label-preview-image {
  max-width: 100%;
  width: auto;
  height: auto;
  max-height: 400px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  object-fit: contain;
}

.dialog-footer {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.loading-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #999;
}

.loading-placeholder .el-icon {
  font-size: 32px;
  margin-bottom: 10px;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #999;
}

.loading-state .el-icon {
  font-size: 32px;
  margin-bottom: 10px;
}

/* Responsive Styles */
@media (max-width: 768px) {
  .card-header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
  
  .header-actions {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .header-actions .el-input {
    width: 100% !important;
  }
  
  .action-card {
    height: auto;
    margin-bottom: 15px;
  }
  
  .card-content {
    height: auto;
  }
  
  .el-table .el-table-column.is-left .cell {
    font-size: 12px;
  }
  
  .pagination-container {
    overflow-x: auto;
  }
  
  .pagination-container .el-pagination {
    justify-content: center;
    flex-wrap: wrap;
  }
}

@media (max-width: 480px) {
  .header-actions {
    align-items: stretch;
  }
  
  .el-table .el-table__body-wrapper {
    overflow-x: auto;
  }
}

/* Pagination Styles */
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

/* Bulk Actions Styles */
.bulk-actions-bar {
  margin-bottom: 15px;
}

.bulk-actions {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-top: 8px;
}

@media (max-width: 480px) {
  .bulk-actions {
    flex-direction: column;
    align-items: stretch;
    gap: 5px;
  }
  
  .bulk-actions .el-button {
    width: 100%;
    margin: 2px 0;
  }
  
  /* Small mobile preview optimization */
  .label-info {
    padding: 8px;
    margin-bottom: 10px;
  }
  
  .label-info h3 {
    font-size: 0.95rem;
  }
  
  .label-info p {
    font-size: 0.8rem;
  }
  
  .label-image-container {
    padding: 8px;
  }
  
  .label-preview-image {
    max-height: 250px;
  }
  
  .dialog-footer .el-button {
    padding: 12px 16px;
    font-size: 14px;
  }
}
</style>