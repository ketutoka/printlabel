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

const router = useRouter()
const userStore = useUserStore()

const isAuthenticated = computed(() => userStore.isAuthenticated)

const logout = () => {
  userStore.logout()
  router.push('/login')
}

onMounted(() => {
  // Check if user is logged in
  if (userStore.token && !userStore.user) {
    userStore.getCurrentUser()
  }
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
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
</style>