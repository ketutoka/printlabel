<template>
  <div class="register-container">
    <el-card class="register-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <h2>🏷️ Daftar Akun - Print Label</h2>
        </div>
      </template>

      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="rules"
        label-width="80px"
        @submit.prevent="handleRegister"
      >
        <el-form-item label="Nama" prop="name">
          <el-input
            v-model="registerForm.name"
            placeholder="Masukkan nama lengkap"
            prefix-icon="User"
          />
        </el-form-item>

        <el-form-item label="Email" prop="email">
          <el-input
            v-model="registerForm.email"
            type="email"
            placeholder="Masukkan email Anda"
            prefix-icon="Message"
          />
        </el-form-item>

        <el-form-item label="No HP" prop="phone">
          <el-input
            v-model="registerForm.phone"
            placeholder="Masukkan nomor HP (contoh: 081234567890)"
            prefix-icon="Phone"
          />
        </el-form-item>

        <el-form-item label="Password" prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="Masukkan password (min. 6 karakter)"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>

        <el-form-item label="Konfirmasi" prop="confirmPassword">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="Konfirmasi password"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            :loading="userStore.loading"
            @click="handleRegister"
            style="width: 100%"
          >
            {{ userStore.loading ? 'Sedang Mendaftar...' : 'Daftar' }}
          </el-button>
        </el-form-item>

        <div class="register-links">
          <el-link type="primary" @click="$router.push('/login')">
            Sudah punya akun? Login disini
          </el-link>
        </div>
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
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()

const registerFormRef = ref()
const registerForm = reactive({
  name: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: ''
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value !== registerForm.password) {
    callback(new Error('Konfirmasi password tidak sama'))
  } else {
    callback()
  }
}

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
  ],
  password: [
    { required: true, message: 'Password harus diisi', trigger: 'blur' },
    { min: 6, message: 'Password minimal 6 karakter', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: 'Konfirmasi password harus diisi', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      const { confirmPassword, ...userData } = registerForm
      const result = await userStore.register(userData)
      
      if (result.success) {
        ElMessage.success('Registrasi berhasil! Silakan login.')
        router.push('/login')
      } else {
        ElMessage.error(result.error || 'Registrasi gagal')
      }
    }
  })
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 10px;
}

.register-card {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
}

.card-header {
  text-align: center;
  color: #409EFF;
}

.card-header h2 {
  margin: 0;
  font-size: 1.5rem;
}

.register-links {
  text-align: center;
  margin-top: 15px;
}

/* Mobile Responsiveness - Full Width */
@media (max-width: 768px) {
  .register-container {
    padding: 5px;
    align-items: flex-start;
    padding-top: 8vh;
  }
  
  .register-card {
    max-width: 100%;
    width: 100%;
  }
  
  .card-header h2 {
    font-size: 1.3rem;
  }
  
  :deep(.el-card) {
    margin: 0;
    border-radius: 8px;
  }
  
  :deep(.el-card__body) {
    padding: 20px;
  }
  
  :deep(.el-form-item) {
    margin-bottom: 18px;
  }
  
  :deep(.el-form-item__label) {
    font-size: 14px;
    width: 90px !important;
    font-weight: 500;
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
  
  :deep(.el-button) {
    padding: 12px 20px;
    font-size: 16px;
    width: 100%;
    box-sizing: border-box;
  }
}

@media (max-width: 480px) {
  .register-container {
    padding: 3px;
    padding-top: 5vh;
  }
  
  .card-header h2 {
    font-size: 1.2rem;
  }
  
  :deep(.el-card__body) {
    padding: 15px;
  }
  
  :deep(.el-form-item__label) {
    font-size: 13px;
    width: 80px !important;
  }
  
  :deep(.el-input__inner) {
    padding: 10px 12px;
    font-size: 16px;
  }
  
  .register-links {
    font-size: 14px;
  }
}

@media (max-width: 360px) {
  .register-container {
    padding: 2px;
  }
  
  :deep(.el-card__body) {
    padding: 12px;
  }
  
  :deep(.el-form-item__label) {
    width: 70px !important;
    font-size: 12px;
  }
}

/* Landscape mobile */
@media (max-width: 896px) and (orientation: landscape) {
  .register-container {
    padding-top: 2vh;
    min-height: 100vh;
  }
  
  :deep(.el-card__body) {
    padding: 15px;
  }
}
</style>