<template>
  <div class="profile-edit-container">
    <el-card class="profile-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <h2>👤 Edit Profil</h2>
        </div>
      </template>

      <el-form
        ref="profileFormRef"
        :model="profileForm"
        :rules="rules"
        label-width="100px"
        @submit.prevent="handleUpdateProfile"
      >
        <el-form-item label="Nama" prop="name">
          <el-input
            v-model="profileForm.name"
            placeholder="Masukkan nama lengkap"
            prefix-icon="User"
          />
        </el-form-item>

        <el-form-item label="Email" prop="email">
          <el-input
            v-model="profileForm.email"
            type="email"
            placeholder="Masukkan email Anda"
            prefix-icon="Message"
          />
        </el-form-item>

        <el-form-item label="No HP" prop="phone">
          <el-input
            v-model="profileForm.phone"
            placeholder="Masukkan nomor HP (contoh: 081234567890)"
            prefix-icon="Phone"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            :loading="userStore.loading"
            @click="handleUpdateProfile"
            style="width: 100%; margin-top: 20px;"
          >
            {{ userStore.loading ? 'Menyimpan...' : '💾 Simpan Perubahan' }}
          </el-button>
        </el-form-item>

        <el-form-item>
          <el-button
            type="default"
            @click="$router.push('/dashboard')"
            style="width: 100%;"
          >
            ↩️ Kembali ke Dashboard
          </el-button>
        </el-form-item>
      </el-form>

      <!-- Error Alert -->
      <el-alert
        v-if="userStore.error"
        :title="userStore.error"
        type="error"
        style="margin-top: 15px"
        show-icon
        @close="userStore.clearError"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()

const profileFormRef = ref()
const profileForm = reactive({
  name: '',
  email: '',
  phone: ''
})

const rules = {
  name: [
    { required: true, message: 'Nama harus diisi', trigger: 'blur' },
    { min: 2, message: 'Nama minimal 2 karakter', trigger: 'blur' }
  ],
  email: [
    { required: true, message: 'Email harus diisi', trigger: 'blur' },
    { type: 'email', message: 'Format email tidak valid', trigger: 'blur' }
  ],
  phone: [
    { required: true, message: 'No HP harus diisi', trigger: 'blur' },
    { min: 10, message: 'No HP minimal 10 digit', trigger: 'blur' },
    { max: 15, message: 'No HP maksimal 15 digit', trigger: 'blur' },
    { pattern: /^[0-9]+$/, message: 'No HP hanya boleh berisi angka', trigger: 'blur' }
  ]
}

const handleUpdateProfile = async () => {
  if (!profileFormRef.value) return
  
  await profileFormRef.value.validate(async (valid) => {
    if (valid) {
      const result = await userStore.updateProfile(profileForm)
      
      if (result.success) {
        ElMessage.success('Profil berhasil diperbarui!')
        router.push('/dashboard')
      } else {
        ElMessage.error(result.error || 'Gagal memperbarui profil')
      }
    }
  })
}

// Load current user data when component mounts
onMounted(async () => {
  // Make sure user data is loaded
  if (!userStore.user && userStore.token) {
    await userStore.getCurrentUser()
  }
  
  if (userStore.user) {
    profileForm.name = userStore.user.name || ''
    profileForm.email = userStore.user.email || ''
    profileForm.phone = userStore.user.phone || ''
  } else {
    // If no user data, redirect to login
    router.push('/login')
  }
})
</script>

<style scoped>
.profile-edit-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.profile-card {
  width: 100%;
  max-width: 500px;
}

.card-header {
  text-align: center;
  color: #409EFF;
}
</style>