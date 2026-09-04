<template>
  <!-- 最外层自定义背景类 login-bg -->
  <div class="min-h-screen flex items-center justify-center px-6 login-bg">
    <div class="w-full max-w-md">
      <!-- 卡片：提高底色透明度，文字更容易看清 -->
      <div class="bg-black/15 backdrop-blur-xl rounded-2xl shadow-card p-8 border border-white/25">
        <!-- 标题文字改为白色 text-white -->
        <h1 class="text-3xl font-bold text-center text-white mb-2">VESTA.OnlineMall</h1>
        <!-- 副标题浅白色 text-white/80 -->
        <p class="text-white/80 text-center text-sm mb-8">登录您的账户以继续购物</p>
        <form @submit.prevent="handleLogin" class="space-y-5">
          <div>
            <!-- 标签文字白色 -->
            <label class="block text-sm text-white/85 mb-1.5">用户名</label>
            <input
              v-model="form.username"
              type="text"
              class="w-full px-4 py-3 rounded-xl border border-white/30 input-focus bg-white/95 text-text-primary"
              placeholder="请输入用户名"
              required
            />
          </div>
          <div>
            <label class="block text-sm text-white/85 mb-1.5">密码</label>
            <input
              v-model="form.password"
              type="password"
              class="w-full px-4 py-3 rounded-xl border border-white/30 input-focus bg-white/95 text-text-primary"
              placeholder="请输入密码"
              required
            />
          </div>
          <!-- 黑色登录按钮！！ -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-gradient-to-r from-yellow-500 to-amber-600 text-white py-3 rounded-xl font-medium btn-transition hover:from-yellow-600 hover:to-amber-700 disabled:opacity-50"
          >
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </form>
        <!-- 底部注册文字改为白色 -->
        <p class="text-center text-sm text-white/75 mt-6">
          还没有账户？
          <router-link to="/register" class="text-white hover:text-white hover:underline">立即注册</router-link>
        </p>
      </div>
    </div>
  </div>
</template>
<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
const form = reactive({
  username: '',
  password: ''
})
const loading = ref(false)
const router = useRouter()
const userStore = useUserStore()
async function handleLogin() {
  loading.value = true
  try {
    await userStore.login(form.username, form.password)
    window.$toast.success('登录成功')
    router.push('/')
  } catch (e) {
    window.$toast.error(e.message)
  } finally {
    loading.value = false
  }
}
</script>
<style scoped>
.login-bg {
  background-image: url("/login-background.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
  /* 暗色蒙版，背景压暗，文字可读性大幅提升 */
  background-color: rgba(0, 0, 0, 0.28);
  background-blend-mode: overlay;
}
</style>
