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
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
}

.card-header {
  text-align: center;
  color: #409EFF;
}

.login-links {
  text-align: center;
  margin-top: 15px;
}

.login-links .el-link {
  margin: 5px 0;
}
</style>