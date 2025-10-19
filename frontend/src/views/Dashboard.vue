<template>
  <div class="dashboard-container">
    <!-- Frozen Header with App Title and Profile -->
    <div class="frozen-header">
      <div class="header-content">
        <div class="app-title">
          <h3>🏷️ Label Thermal Printer</h3>
        </div>
        <div class="profile-section">
          <el-dropdown @command="handleCommand" placement="bottom-end" trigger="click" :hide-on-click="true">
            <div class="profile-trigger" title="Menu Profil">
              <el-avatar 
                :size="36" 
                style="background: linear-gradient(135deg, #409EFF, #66b3ff); color: white; cursor: pointer; border: 2px solid rgba(255, 255, 255, 0.3);"
              >
                <el-icon><User /></el-icon>
              </el-avatar>
            </div>
            <template #dropdown>
              <el-dropdown-menu class="profile-dropdown">
                <el-dropdown-item disabled class="user-info-item">
                  <div class="user-info-content">
                    <el-avatar 
                      :size="32" 
                      style="background: linear-gradient(135deg, #409EFF, #66b3ff); margin-bottom: 8px;"
                    >
                      <el-icon><User /></el-icon>
                    </el-avatar>
                    <div class="user-details">
                      <div class="user-name">{{ userStore.user?.name || 'User' }}</div>
                      <div class="user-email">{{ userStore.user?.email }}</div>
                    </div>
                  </div>
                </el-dropdown-item>
                <el-dropdown-item divided command="profile" class="menu-item">
                  <el-icon class="menu-icon"><Setting /></el-icon>
                  <span>Edit Profil</span>
                </el-dropdown-item>
                <el-dropdown-item command="logout" class="menu-item logout-item">
                  <el-icon class="menu-icon"><SwitchButton /></el-icon>
                  <span>Logout</span>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </div>
    
    <el-row :gutter="20">
      <!-- Welcome Card -->
      <el-col :span="24">
        <el-card shadow="hover" style="margin-bottom: 20px;">
          <div class="welcome-section">
            <h2>👋 Selamat Datang, {{ userStore.user?.name || 'User' }}!</h2>
            <p>Kelola dan cetak label paket dengan QR Code untuk thermal printer 58mm dan 80mm</p>
          </div>
        </el-card>
      </el-col>

      <!-- Quick Actions - Responsive Grid -->
      <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
        <el-card shadow="hover" class="action-card">
          <template #header>
            <div class="card-header">
              <span>🏷️ Buat Label Pengiriman</span>
            </div>
          </template>
          <div class="card-content">
            <p>Buat dan cetak label paket dengan QR Code. Penerima dan resi bersifat opsional.</p>
            <el-button 
              type="primary" 
              size="large"
              @click="$router.push('/create-shipping-label')"
              style="width: 100%; margin-top: 15px;"
            >
              🏷️ Buat Label
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
              <el-button type="primary" @click="$router.push('/create-shipping-label')">
                Buat Label Pertama
              </el-button>
            </el-empty>
          </div>

          <div v-else>
            <!-- Bulk Actions Bar -->
            <div v-if="selectedLabels.length > 0" class="bulk-actions-bar">
              <el-alert
                :title="selectedLabels.length + ' label dipilih'"
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
              <el-table-column prop="label_size" label="Ukuran" width="100">
                <template #default="scope">
                  <el-tag :type="scope.row.label_size === '58mm' ? 'success' : 'warning'">
                    {{ scope.row.label_size || '58mm' }} <!-- Debug: Show actual value -->
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="shipping_code" label="Kode/Resi" width="180">
                <template #default="scope">
                  {{ scope.row.shipping_code ? scope.row.shipping_code.toUpperCase() : '(Tanpa Resi)' }}
                </template>
              </el-table-column>
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
            title="Hari Ini" 
            :value="todayLabelsCount"
            prefix="📅"
          />
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card shadow="hover" class="stat-card">
          <el-statistic 
            title="Minggu Ini" 
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
          <h3>📦 {{ previewLabelData.shipping_code ? previewLabelData.shipping_code.toUpperCase() : 'LABEL' }}</h3>
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
  // Gunakan hanya shipping labels (unified system)
  const shippingLabels = shippingStore.shippingLabels.map(label => {
    // Debug: Log label data untuk melihat label_size
    console.log('Label data:', {
      id: label.id,
      sender_name: label.sender_name,
      label_size: label.label_size,
      shipping_code: label.shipping_code
    })
    
    return {
      ...label,
      display_name: label.recipient_name ? 
        `${label.sender_name} → ${label.recipient_name}` : 
        label.sender_name || 'Label',
      shipping_code: label.shipping_code ? label.shipping_code.toUpperCase() : '(Tanpa Resi)'
    }
  })
  
  // Urutkan berdasarkan tanggal terbaru
  return shippingLabels
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
    // Use shipping store for unified system
    const result = await shippingStore.getShippingLabelForPrint(label.id)
    
    if (result.success) {
      // Detect mobile device
      const isMobileDevice = window.innerWidth <= 768 || /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
      
      if (isMobileDevice) {
        // Mobile: Show mobile-friendly options
        ElMessageBox.confirm(
          'Pilih cara mencetak label di mobile:',
          'Opsi Printing Mobile',
          {
            distinguishCancelAndClose: true,
            confirmButtonText: '�️ Print Label (Gambar)',
            cancelButtonText: '⬇️ Download PNG',
            type: 'info',
          }
        ).then(() => {
          // Use same print method as desktop but optimized for mobile
          printViaBrowser(label)
        }).catch((action) => {
          if (action === 'cancel') {
            // Download image
            downloadLabel(label)
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
          printViaBrowser(label)
        }).catch((action) => {
          if (action === 'cancel') {
            // Download image
            downloadLabel(label)
          }
        })
      }
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
    // Get the preview image URL using shipping store (unified system)
    const token = userStore.token
    const imageUrl = `${api.defaults.baseURL}/shipping-labels/preview/${label.id}?token=${token}`
    
    // Detect if mobile for different layout
    const isMobileDevice = window.innerWidth <= 768 || /Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)
    
    // Create a new window for printing
    const printWindow = window.open('', '_blank')
    const labelCode = label.shipping_code || 'Label'
    
    // Write basic HTML structure
    printWindow.document.write('<!DOCTYPE html>')
    printWindow.document.write('<html><head>')
    printWindow.document.write(`<title>Print Label - ${labelCode}</title>`)
    printWindow.document.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    
    // Add CSS styles
    const styles = `
      <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        @page { margin: 0; size: 58mm 100mm; }
        html, body { margin: 0; padding: 0; background: white; font-family: Arial, sans-serif; }
        .print-container {
          display: flex; flex-direction: column; align-items: center;
          justify-content: ${isMobileDevice ? 'flex-start' : 'center'};
          min-height: 100vh; padding: ${isMobileDevice ? '20px' : '2mm'};
        }
        .label-info {
          text-align: center; margin-bottom: 20px;
          display: ${isMobileDevice ? 'block' : 'none'};
        }
        .label-info h2 { color: #409EFF; margin-bottom: 10px; font-size: 18px; }
        .label-info p { margin: 5px 0; color: #666; font-size: 14px; }
        img { max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .mobile-print-buttons {
          display: ${isMobileDevice ? 'flex' : 'none'};
          flex-direction: row; gap: 15px; margin: 20px 0; justify-content: center; flex-wrap: wrap;
        }
        .print-button, .download-button { 
          padding: 12px 24px; border: none; border-radius: 6px; font-size: 14px; font-weight: 500; 
          cursor: pointer; text-decoration: none; display: inline-flex; align-items: center; 
          gap: 8px; transition: all 0.3s ease; min-width: 120px; justify-content: center; 
        }
        .print-button { background: linear-gradient(135deg, #409EFF, #66b3ff); color: white; box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3); }
        .download-button { background: linear-gradient(135deg, #67C23A, #85ce61); color: white; box-shadow: 0 4px 12px rgba(103, 194, 58, 0.3); }
        .print-instructions {
          display: ${isMobileDevice ? 'block' : 'none'};
          margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #409EFF; 
          font-size: 14px; line-height: 1.6; color: #555; max-width: 400px;
        }
        @media print {
          @page { margin: 0 !important; size: 58mm auto !important; }
          html, body { width: 58mm !important; max-width: 58mm !important; margin: 0 !important; padding: 0 !important; background: white !important; font-size: 12px !important; }
          .mobile-print-buttons, .print-instructions, .label-info { display: none !important; }
          .print-container { min-height: auto !important; height: auto !important; padding: 1mm !important; margin: 0 !important; justify-content: flex-start !important; align-items: center !important; width: 58mm !important; max-width: 58mm !important; box-sizing: border-box !important; }
          img { width: 56mm !important; max-width: 56mm !important; height: auto !important; border: none !important; padding: 0 !important; margin: 0 auto !important; page-break-inside: avoid !important; object-fit: contain !important; display: block !important; box-sizing: border-box !important; }
        }
        @media screen and (max-width: 768px) {
          body { width: 100vw !important; max-width: 100vw !important; }
          .print-container { padding: 15px; width: 100% !important; max-width: 100% !important; min-height: auto; }
          img { max-width: 280px; width: 100%; }
          .mobile-print-buttons { flex-direction: column; gap: 8px; }
          .print-button, .download-button { width: 100%; max-width: 280px; padding: 14px 20px; font-size: 16px; }
        }
      </style>
    `
    printWindow.document.write(styles)
    printWindow.document.write('</head><body>')
    
    // Add body content
    printWindow.document.write('<div class="print-container">')
    printWindow.document.write('<div class="label-info">')
    printWindow.document.write(`<h2>🏷️ Label Pengiriman (${label.label_size || '58mm'})</h2>`)
    printWindow.document.write(`<p><strong>Kode:</strong> ${labelCode}</p>`)
    printWindow.document.write(`<p><strong>Pengirim:</strong> ${label.sender_name || 'Tidak ada'}</p>`)
    if (label.recipient_name) {
      printWindow.document.write(`<p><strong>Penerima:</strong> ${label.recipient_name}</p>`)
    }
    printWindow.document.write(`<p><strong>Ukuran:</strong> ${label.label_size || '58mm'}</p>`)
    printWindow.document.write(`<p><strong>Tanggal:</strong> ${new Date(label.created_at).toLocaleDateString('id-ID')}</p>`)
    printWindow.document.write('</div>')
    
    // Add image with onload handler
    const onloadHandler = isMobileDevice 
      ? "console.log('Image loaded');" 
      : "window.print(); setTimeout(function() { window.close(); }, 1000);"
    
    printWindow.document.write(`<img src="${imageUrl}" alt="Label ${labelCode}" onload="setTimeout(function() { ${onloadHandler} }, 500);" onerror="alert('Error loading image');" />`)
    
    // Add mobile buttons
    printWindow.document.write('<div class="mobile-print-buttons">')
    printWindow.document.write('<button class="print-button" onclick="window.print()">🖨️ Cetak Label</button>')
    printWindow.document.write(`<a href="${imageUrl}" download="${labelCode}.png" class="download-button">⬇️ Download PNG</a>`)
    printWindow.document.write('</div>')
    
    // Add instructions
    printWindow.document.write('<div class="print-instructions">')
    printWindow.document.write('<strong>📱 Cara Print:</strong><br>')
    printWindow.document.write('1. Tekan tombol "Cetak Label" di atas<br>')
    printWindow.document.write('2. Pilih printer yang tersedia<br>')
    printWindow.document.write('3. Pastikan ukuran kertas sesuai (A4 atau 58mm untuk thermal)<br>')
    printWindow.document.write('4. Klik Print untuk mencetak label<br>')
    printWindow.document.write('5. Atau download PNG untuk print dari aplikasi lain')
    printWindow.document.write('</div>')
    printWindow.document.write('</div>')
    
    // Add optimization script
    printWindow.document.write('<script>')
    printWindow.document.write('function optimizePrint() {')
    printWindow.document.write('  window.addEventListener("beforeprint", function() {')
    printWindow.document.write('    document.body.style.width = "58mm";')
    printWindow.document.write('    document.body.style.maxWidth = "58mm";')
    printWindow.document.write('    document.body.style.overflow = "hidden";')
    printWindow.document.write('    var container = document.querySelector(".print-container");')
    printWindow.document.write('    if (container) {')
    printWindow.document.write('      container.style.width = "58mm";')
    printWindow.document.write('      container.style.maxWidth = "58mm";')
    printWindow.document.write('    }')
    printWindow.document.write('    var img = document.querySelector("img");')
    printWindow.document.write('    if (img) {')
    printWindow.document.write('      img.style.width = "56mm";')
    printWindow.document.write('      img.style.maxWidth = "56mm";')
    printWindow.document.write('      img.style.height = "auto";')
    printWindow.document.write('    }')
    printWindow.document.write('  });')
    printWindow.document.write('  window.addEventListener("afterprint", function() {')
    printWindow.document.write('    document.body.style.width = "";')
    printWindow.document.write('    document.body.style.maxWidth = "";')
    printWindow.document.write('    document.body.style.overflow = "";')
    printWindow.document.write('  });')
    printWindow.document.write('}')
    printWindow.document.write('document.addEventListener("DOMContentLoaded", optimizePrint);')
    printWindow.document.write('if (document.readyState === "complete") { optimizePrint(); }')
    printWindow.document.write('</' + 'script>')
    
    printWindow.document.write('</' + 'body>')
    printWindow.document.write('</' + 'html>')
    printWindow.document.close()
    
    ElMessage.success(`Label ${labelCode} dikirim ke printer!`)
  } catch (error) {
    ElMessage.error('Gagal mencetak label')
    console.error('Print error:', error)
  }
}

const downloadLabel = async (label) => {
  try {
    const token = userStore.token
    // Use shipping store endpoint (unified system)
    const imageUrl = `${api.defaults.baseURL}/shipping-labels/preview/${label.id}?token=${token}`
    
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
    
    // Get preview URL using shipping store (unified system)
    previewImageUrl.value = await shippingStore.getPreviewUrl(label.id)
    
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
    // Fetch only shipping labels (unified system)
    const shippingResult = await shippingStore.fetchShippingLabels()
    
    if (shippingResult.success) {
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
  
  // Load shipping labels (unified system) if user is authenticated
  if (userStore.isAuthenticated) {
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
    
    // Delete shipping label (unified system)
    const result = await shippingStore.deleteShippingLabel(label.id)
    
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
    
    // Bulk delete shipping labels (unified system)
    const labelIds = selectedLabels.value.map(label => label.id)
    const result = await shippingStore.bulkDeleteShippingLabels(labelIds)
    
    // Clear selection after deletion attempt
    selectedLabels.value = []
    
    // Show results
    if (result.success) {
      const deleted = result.results.deleted_count || labelIds.length
      ElMessage.success(`${deleted} label berhasil dihapus!`)
    } else {
      ElMessage.error(`Gagal menghapus label: ${result.error}`)
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
/* Frozen Header Styles */
.frozen-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  z-index: 1000;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 12px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-title h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: white;
}

.profile-section {
  display: flex;
  align-items: center;
}

.profile-trigger {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 4px;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.profile-trigger:hover {
  background-color: rgba(255, 255, 255, 0.1);
  transform: scale(1.05);
}

/* Profile Dropdown Styles */
:deep(.profile-dropdown) {
  min-width: 220px;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  border: 1px solid #e4e7ed;
  overflow: hidden;
}

:deep(.user-info-item) {
  padding: 16px !important;
  background: linear-gradient(135deg, #f8f9fa, #ffffff);
  border-bottom: 1px solid #e4e7ed;
}

.user-info-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.user-details {
  margin-top: 4px;
}

.user-name {
  font-weight: 600;
  color: #303133;
  font-size: 14px;
  margin-bottom: 2px;
}

.user-email {
  font-size: 12px;
  color: #909399;
}

:deep(.menu-item) {
  padding: 12px 16px !important;
  display: flex !important;
  align-items: center !important;
  transition: all 0.3s ease;
}

:deep(.menu-item:hover) {
  background-color: #f5f7fa;
  color: #409EFF;
}

:deep(.logout-item:hover) {
  background-color: #fef0f0;
  color: #F56C6C;
}

.menu-icon {
  margin-right: 10px;
  font-size: 16px;
}

:deep(.menu-item span) {
  font-size: 14px;
  font-weight: 500;
}

.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 80px 10px 10px 10px; /* Add top padding for frozen header */
}

/* Global smooth scrolling */
:deep(html) {
  scroll-behavior: smooth;
}

/* Add subtle entrance animation */
.dashboard-container {
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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
  .frozen-header .header-content {
    padding: 10px 15px;
  }
  
  .app-title h3 {
    font-size: 14px;
    font-weight: 500;
  }
  
  .profile-trigger .el-avatar {
    width: 32px !important;
    height: 32px !important;
  }
  
  .dashboard-container {
    padding: 70px 5px 5px 5px; /* Adjust top padding for mobile header */
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
  .frozen-header .header-content {
    padding: 8px 10px;
  }
  
  .app-title h3 {
    font-size: 12px;
    line-height: 1.2;
  }
  
  .dashboard-container {
    padding: 65px 3px 3px 3px;
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