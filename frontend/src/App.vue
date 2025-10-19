<template>
  <div id="app">
    <el-container style="height: 100vh">
      <!-- Header Navigation -->
      <el-header v-if="isAuthenticated" style="background-color: #409EFF; color: white;">
        <div class="header-content">
          <h2>🏷️ Print Label App</h2>
          <div class="user-info">
            <span>Halo, {{ userStore.user?.name }}</span>
            <el-button @click="logout" type="danger" size="small" style="margin-left: 15px">
              Logout
            </el-button>
          </div>
        </div>
      </el-header>

      <!-- Main Content -->
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from './stores/user'
import { useShippingStore } from './stores/shipping'

const router = useRouter()
const userStore = useUserStore()
const shippingStore = useShippingStore()

const isAuthenticated = computed(() => userStore.isAuthenticated)

const logout = () => {
  userStore.logout()
  router.push('/login')
}

onMounted(() => {
  // Check if user is logged in
  if (userStore.token && !userStore.user) {
    userStore.getCurrentUser().then(() => {
      // Load shipping labels after user info is loaded
      if (userStore.isAuthenticated) {
        shippingStore.fetchShippingLabels()
      }
    })
  } else if (userStore.isAuthenticated) {
    // If user is already loaded, just load shipping labels
    shippingStore.fetchShippingLabels()
  }
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  width: 100%;
  overflow-x: hidden;
}

/* Global mobile optimizations */
@media (max-width: 768px) {
  /* Prevent horizontal scrolling on mobile */
  html, body, #app {
    max-width: 100vw !important;
    overflow-x: hidden !important;
    margin: 0 !important;
    padding: 0 !important;
  }
  
  /* Make all containers full width */
  .el-container,
  .el-main,
  .el-card,
  .el-form {
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 !important;
    box-sizing: border-box !important;
  }
  
  /* Reset any margin/padding that might create gaps */
  .el-main {
    padding: 5px !important;
  }
  
  /* Force all page containers to full width */
  .create-label-container,
  .login-container,
  .register-container,
  .create-shipping-label-container,
  .dashboard-container {
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 !important;
    padding: 3px !important;
    box-sizing: border-box !important;
  }
  
  /* Ensure form inputs use full available width */
  .el-form-item,
  .el-input,
  .el-textarea,
  .el-select {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
  }
  
  /* Force input elements to be full width */
  .el-input__wrapper,
  .el-input__inner,
  .el-textarea__inner {
    width: 100% !important;
    box-sizing: border-box !important;
  }
  
  /* Prevent iOS zoom on input focus */
  input, textarea, select {
    font-size: 16px !important;
  }
  
  /* Make buttons touch-friendly */
  .el-button {
    min-height: 44px;
    font-size: 16px;
  }
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.user-info {
  display: flex;
  align-items: center;
}

.el-main {
  padding: 20px;
  background-color: #f5f5f5;
}

/* Mobile header adjustments */
@media (max-width: 768px) {
  .header-content h2 {
    font-size: 18px;
  }
  
  .user-info span {
    font-size: 14px;
    margin-right: 8px;
  }
  
  .user-info .el-button {
    font-size: 12px;
    padding: 8px 12px;
  }
}
</style>