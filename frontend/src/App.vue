<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader v-if="!isAuthPage" />
    <main class="flex-1">
      <transition name="fade" mode="out-in">
        <router-view />
      </transition>
    </main>
    <ToastContainer />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppHeader from './components/AppHeader.vue'
import ToastContainer from './components/ToastContainer.vue'
import { useUserStore } from './stores/user'
import { useCartStore } from './stores/cart'

const route = useRoute()
const userStore = useUserStore()
const cartStore = useCartStore()

const isAuthPage = computed(() => {
  return route.path === '/login' || route.path === '/register'
})

// 初始化时如果有token，拉取用户信息和购物车
async function init() {
  if (userStore.isLoggedIn) {
    try {
      await userStore.fetchUserInfo()
      await cartStore.refreshCart()
    } catch (e) {
      console.error('应用初始化失败', e)
    }
  }
}

init()
</script>
