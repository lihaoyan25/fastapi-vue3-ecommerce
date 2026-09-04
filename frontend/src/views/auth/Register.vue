<template>
  <div class="min-h-screen flex items-center justify-center px-6 login-bg">
    <div class="w-full max-w-md">
      <div class="bg-black/15 backdrop-blur-xl rounded-2xl shadow-card p-8 border border-white/25">
        <h1 class="text-2xl font-bold text-center text-white mb-2">创建账户</h1>
        <p class="text-white/80 text-center text-sm mb-8">注册VESTA.OnlineMall即送 1000 CNY体验金</p>
        <form @submit.prevent="handleRegister" class="space-y-4">
          <div>
            <label class="block text-sm text-white/85 mb-1.5">用户名</label>
            <input
              v-model="form.username"
              type="text"
              class="w-full px-4 py-3 rounded-xl border border-white/30 input-focus bg-white/95 text-text-primary"
              placeholder="字母开头, 3-20位字母数字下划线"
              required
            />
          </div>
          <div>
            <label class="block text-sm text-white/85 mb-1.5">邮箱</label>
            <input
              v-model="form.email"
              type="email"
              class="w-full px-4 py-3 rounded-xl border border-white/30 input-focus bg-white/95 text-text-primary"
              placeholder="请输入邮箱"
              required
            />
          </div>
          <div>
            <label class="block text-sm text-white/85 mb-1.5">手机号</label>
            <input
              v-model="form.phone"
              type="tel"
              class="w-full px-4 py-3 rounded-xl border border-white/30 input-focus bg-white/95 text-text-primary"
              placeholder="请输入11位手机号"
            />
          </div>
          <div>
            <label class="block text-sm text-white/85 mb-1.5">密码</label>
            <input
              v-model="form.password"
              type="password"
              class="w-full px-4 py-3 rounded-xl border border-white/30 input-focus bg-white/95 text-text-primary"
              placeholder="8-20位，包含大小写字母和数字"
              required
            />
          </div>
          <div>
            <label class="block text-sm text-white/85 mb-1.5">确认密码</label>
            <input
              v-model="form.password_confirm"
              type="password"
              class="w-full px-4 py-3 rounded-xl border border-white/30 input-focus bg-white/95 text-text-primary"
              placeholder="请再次输入密码"
              required
            />
          </div>
          <!-- 和登录一模一样的香槟金色渐变按钮 -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-gradient-to-r from-yellow-500 to-amber-600 text-white py-3 rounded-xl font-medium btn-transition hover:from-yellow-600 hover:to-amber-700 disabled:opacity-50"
          >
            {{ loading ? '注册中...' : '注册' }}
          </button>
        </form>
        <p class="text-center text-sm text-white/75 mt-6">
          已有账户？
          <router-link to="/login" class="text-white hover:text-white hover:underline">立即登录</router-link>
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
  email: '',
  phone: '',
  password: '',
  password_confirm: ''
})
const loading = ref(false)
const router = useRouter()
const userStore = useUserStore()
async function handleRegister() {
  if (form.password !== form.password_confirm) {
    window.$toast.error('两次密码输入不一致')
    return
  }
  loading.value = true
  try {
    await userStore.register(form)
    window.$toast.success('注册成功，请登录')
    router.push('/login')
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
  background-color: rgba(0, 0, 0, 0.28);
  background-blend-mode: overlay;
}
</style>
