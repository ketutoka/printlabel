<template>
  <div class="login-container">
    <el-card class="login-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <h2>🏷️ Login - Print Label</h2>
        </div>
      </template>

      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="rules"
        label-width="80px"
        @submit.prevent="handleLogin"
      >
        <el-form-item label="Email" prop="email">
          <el-input
            v-model="loginForm.email"
            type="email"
            placeholder="Masukkan email Anda"
            prefix-icon="Message"
          />
        </el-form-item>

        <el-form-item label="Password" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="Masukkan password Anda"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            :loading="userStore.loading"
            @click="handleLogin"
            style="width: 100%"
          >
            {{ userStore.loading ? 'Sedang Login...' : 'Login' }}
          </el-button>
        </el-form-item>

        <div class="login-links">
          <el-link type="primary" @click="$router.push('/register')">
            Belum punya akun? Daftar disini
          </el-link>
          <br>
          <el-link type="info" @click="$router.push('/reset-password')">
            Lupa password?
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

const loginFormRef = ref()
const loginForm = reactive({
  email: '',
  password: ''
})

const rules = {
  email: [
    { required: true, message: 'Email harus diisi', trigger: 'blur' },
    { type: 'email', message: 'Format email tidak valid', trigger: 'blur' }
  ],
  password: [
    { required: true, message: 'Password harus diisi', trigger: 'blur' },
    { min: 6, message: 'Password minimal 6 karakter', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      const result = await userStore.login(loginForm)
      
      if (result.success) {
        ElMessage.success('Login berhasil!')
        router.push('/dashboard')
      } else {
        ElMessage.error(result.error || 'Login gagal')
      }
    }
  })
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 10px;
}

.login-card {
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

.login-links {
  text-align: center;
  margin-top: 15px;
}

.login-links .el-link {
  margin: 5px 0;
}

/* Mobile Responsiveness - Full Width */
@media (max-width: 768px) {
  .login-container {
    padding: 3px !important;
    align-items: flex-start;
    padding-top: 5vh;
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 !important;
  }
  
  .login-card {
    max-width: 100% !important;
    width: 100% !important;
    margin: 0 !important;
    box-sizing: border-box;
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
    width: 80px !important;
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
  .login-container {
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
    width: 70px !important;
  }
  
  :deep(.el-input__inner) {
    padding: 10px 12px;
    font-size: 16px;
  }
  
  .login-links {
    font-size: 14px;
  }
}

@media (max-width: 360px) {
  .login-container {
    padding: 2px;
  }
  
  :deep(.el-card__body) {
    padding: 12px;
  }
  
  :deep(.el-form-item__label) {
    width: 60px !important;
    font-size: 12px;
  }
}

/* Landscape mobile */
@media (max-width: 896px) and (orientation: landscape) {
  .login-container {
    padding-top: 2vh;
    min-height: 100vh;
  }
  
  :deep(.el-card__body) {
    padding: 15px;
  }
}
</style>