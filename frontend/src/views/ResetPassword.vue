<template>
  <div class="reset-password-container">
    <el-card class="reset-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <h2>🔐 Reset Password</h2>
        </div>
      </template>

      <el-form
        ref="resetFormRef"
        :model="resetForm"
        :rules="rules"
        label-width="80px"
        @submit.prevent="handleResetPassword"
      >
        <el-form-item label="Email" prop="email">
          <el-input
            v-model="resetForm.email"
            type="email"
            placeholder="Masukkan email Anda"
            prefix-icon="Message"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            :loading="userStore.loading"
            @click="handleResetPassword"
            style="width: 100%"
          >
            {{ userStore.loading ? 'Mengirim...' : 'Kirim Reset Token' }}
          </el-button>
        </el-form-item>

        <div class="reset-links">
          <el-link type="primary" @click="$router.push('/login')">
            Kembali ke Login
          </el-link>
        </div>
      </el-form>

      <!-- Success Alert -->
      <el-alert
        v-if="showSuccess"
        title="Reset token berhasil dikirim ke email Anda!"
        type="success"
        style="margin-top: 15px"
        show-icon
        :closable="false"
      />

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

const resetFormRef = ref()
const showSuccess = ref(false)

const resetForm = reactive({
  email: ''
})

const rules = {
  email: [
    { required: true, message: 'Email harus diisi', trigger: 'blur' },
    { type: 'email', message: 'Format email tidak valid', trigger: 'blur' }
  ]
}

const handleResetPassword = async () => {
  if (!resetFormRef.value) return
  
  await resetFormRef.value.validate(async (valid) => {
    if (valid) {
      const result = await userStore.resetPassword(resetForm.email)
      
      if (result.success) {
        showSuccess.value = true
        ElMessage.success('Reset token berhasil dikirim!')
        
        // Redirect to login after 3 seconds
        setTimeout(() => {
          router.push('/login')
        }, 3000)
      } else {
        ElMessage.error(result.error || 'Reset password gagal')
      }
    }
  })
}
</script>

<style scoped>
.reset-password-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.reset-card {
  width: 100%;
  max-width: 400px;
}

.card-header {
  text-align: center;
  color: #409EFF;
}

.reset-links {
  text-align: center;
  margin-top: 15px;
}
</style>