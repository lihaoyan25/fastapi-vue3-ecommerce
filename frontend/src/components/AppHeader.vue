<template>
  <header class="sticky top-0 z-40 backdrop-blur-xl border-b border-border-light"
          style="background: linear-gradient(90deg, rgba(244,246,249,0.85), rgba(248,245,238,0.85));">
    <div class="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
      <!-- Logo -->
      <router-link to="/" class="text-3xl font-bold text-text-primary btn-transition">
        VESTA.
      </router-link>
      <!-- 导航菜单 -->
      <nav class="flex items-center gap-8">
        <router-link
          to="/"
          class="text-sm text-text-secondary hover:text-text-primary btn-transition"
        >
          商品
        </router-link>
        <router-link
          v-if="userStore.isAdmin"
          to="/admin/products"
          class="text-sm text-text-secondary hover:text-text-primary btn-transition"
        >
          管理后台
        </router-link>
        <!-- 购物车 -->
        <router-link to="/cart" class="relative btn-transition">
          <svg class="w-5 h-5 text-text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          <span
            v-if="cartStore.totalQuantity > 0"
            class="absolute -top-1.5 -right-1.5 bg-gradient-to-r from-yellow-500 to-amber-600 text-white text-xs w-4 h-4 rounded-full flex items-center justify-center"
          >
            {{ cartStore.totalQuantity > 99 ? '99+' : cartStore.totalQuantity }}
          </span>
        </router-link>
        <!-- 用户菜单 -->
        <div ref="menuRef" class="relative" v-if="userStore.isLoggedIn">
          <button
            @click="showMenu = !showMenu"
            class="flex items-center gap-2 text-sm text-text-secondary hover:text-text-primary btn-transition"
          >
            <span>{{ userStore.userInfo?.username }}</span>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <!-- 下拉菜单 -->
          <transition name="dropdown">
            <div
              v-if="showMenu"
              class="absolute right-0 top-full mt-2 w-40 bg-white rounded-xl shadow-card border border-border-light py-1"
            >
              <router-link
                to="/profile"
                class="block px-4 py-2.5 text-sm text-text-primary hover:bg-gray-bg btn-transition"
                @click="showMenu = false"
              >
                个人中心
              </router-link>
              <button
                @click="handleLogout"
                class="w-full text-left px-4 py-2.5 text-sm text-danger hover:bg-gray-bg btn-transition"
              >
                退出登录
              </button>
            </div>
          </transition>
        </div>
        <!-- 未登录 -->
        <template v-else>
          <router-link
            to="/login"
            class="text-sm text-text-secondary hover:text-text-primary btn-transition"
          >
            登录
          </router-link>
          <router-link
            to="/register"
            class="text-sm bg-gradient-to-r from-yellow-500 to-amber-600 text-white px-4 py-1.5 rounded-full btn-transition hover:from-yellow-600 hover:to-amber-700"
          >
            注册
          </router-link>
        </template>
      </nav>
    </div>
  </header>
</template>
<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useUserStore } from '../stores/user'
import { useCartStore } from '../stores/cart'
import { useRouter } from 'vue-router'
const userStore = useUserStore()
const cartStore = useCartStore()
const router = useRouter()
const showMenu = ref(false)
const menuRef = ref(null)
// 点击外部关闭菜单
function handleClickOutside(e) {
  if (menuRef.value && !menuRef.value.contains(e.target)) {
    showMenu.value = false
  }
}
function handleLogout() {
  userStore.logout()
  showMenu.value = false
  window.$toast.success('已退出登录')
  router.push('/login')
}
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  if (userStore.isLoggedIn) {
    cartStore.refreshCart().catch(() => {})
  }
})
onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>
<style scoped>
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}
.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
