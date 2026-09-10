<template>
  <!-- 与登录/注册一致的自定义背景类 login-bg -->
  <div class="min-h-screen flex items-center justify-center px-6 login-bg">
    <div class="w-full max-w-md">
      <div class="bg-black/15 backdrop-blur-xl rounded-2xl shadow-card p-8 border border-white/25">
        <h1 class="text-2xl font-bold text-center text-white mb-2">重置密码</h1>
        <p class="text-white/80 text-center text-sm mb-8">通过账号与绑定手机号验证身份</p>
        <form @submit.prevent="handleReset" class="space-y-4">
          <div>
            <label class="block text-sm text-white/85 mb-1.5">账号</label>
            <input
              v-model="form.account"
              type="text"
              class="w-full px-4 py-3 rounded-xl border border-white/30 input-focus bg-white/95 text-text-primary"
              placeholder="用户名或邮箱"
              required
            />
          </div>
          <div>
            <label class="block text-sm text-white/85 mb-1.5">手机号</label>
            <input
              v-model="form.phone"
              type="tel"
              class="w-full px-4 py-3 rounded-xl border border-white/30 input-focus bg-white/95 text-text-primary"
              placeholder="注册时绑定的11位手机号"
              required
            />
          </div>
          <div>
            <label class="block text-sm text-white/85 mb-1.5">新密码</label>
            <input
              v-model="form.new_password"
              type="password"
              class="w-full px-4 py-3 rounded-xl border border-white/30 input-focus bg-white/95 text-text-primary"
              placeholder="8-20位，包含大小写字母和数字"
              required
            />
          </div>
          <div>
            <label class="block text-sm text-white/85 mb-1.5">确认新密码</label>
            <input
              v-model="form.password_confirm"
              type="password"
              class="w-full px-4 py-3 rounded-xl border border-white/30 input-focus bg-white/95 text-text-primary"
              placeholder="请再次输入新密码"
              required
            />
          </div>
          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-gradient-to-r from-yellow-500 to-amber-600 text-white py-3 rounded-xl font-medium btn-transition hover:from-yellow-600 hover:to-amber-700 disabled:opacity-50"
          >
            {{ loading ? '重置中...' : '重置密码' }}
          </button>
        </form>
        <p class="text-center text-sm text-white/75 mt-6">
          想起密码了？
          <router-link to="/login" class="text-white hover:text-white hover:underline">返回登录</router-link>
        </p>
      </div>
    </div>
  </div>
</template>
<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { forgotPassword } from '../../api/auth'
const form = reactive({
  account: '',
  phone: '',
  new_password: '',
  password_confirm: ''
})
const loading = ref(false)
const router = useRouter()
async function handleReset() {
  if (form.new_password !== form.password_confirm) {
    window.$toast.error('两次密码输入不一致')
    return
  }
  loading.value = true
  try {
    await forgotPassword(form)
    window.$toast.success('密码重置成功，请使用新密码登录')
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
  /* 暗色蒙版，背景压暗，文字可读性大幅提升 */
  background-color: rgba(0, 0, 0, 0.28);
  background-blend-mode: overlay;
}
</style>
