<template>
  <!-- 灰金奢华渐变背景外层容器 -->
  <div class="gradient-bg min-h-screen">
    <div class="max-w-2xl mx-auto px-6 py-10">
      <h1 class="text-2xl font-semibold text-text-primary mb-8">个人中心</h1>
      <div v-if="userStore.userInfo" class="bg-white rounded-2xl shadow-card p-8">
        <!-- 基本信息 -->
        <div class="flex items-center gap-6 pb-6 border-b border-border-light mb-6">
          <div class="w-16 h-16 rounded-full bg-gray-bg flex items-center justify-center text-2xl">
            👤
          </div>
          <div>
            <h2 class="text-xl font-medium text-text-primary">{{ userStore.userInfo.username }}</h2>
            <p class="text-text-secondary text-sm">{{ userStore.userInfo.email }}</p>
            <p class="text-xs mt-1" :class="userStore.isAdmin ? 'text-primary' : 'text-text-tertiary'">
              {{ userStore.isAdmin ? '管理员' : '普通用户' }}
            </p>
          </div>
        </div>
        <!-- 余额 -->
        <div class="mb-8">
          <p class="text-text-secondary text-sm mb-1">账户余额</p>
          <p class="text-3xl font-bold text-text-primary">{{ formatPrice(userStore.userInfo.balance) }}</p>
        </div>
        <!-- 充值 -->
        <div class="mb-8">
          <h3 class="font-medium text-text-primary mb-3">账户充值</h3>
          <div class="flex gap-3">
            <input
              v-model="rechargeAmount"
              type="number"
              min="1"
              class="flex-1 px-4 py-2.5 rounded-xl border border-border-light input-focus"
              placeholder="输入充值金额"
            />
            <button
              @click="handleRecharge"
              :disabled="recharging"
              class="px-6 py-2.5 bg-gradient-to-r from-yellow-500 to-amber-600 text-white rounded-xl btn-transition hover:from-yellow-600 hover:to-amber-700 disabled:opacity-50"
            >
              {{ recharging ? '充值中...' : '充值' }}
            </button>
          </div>
        </div>
        <!-- 其他信息 -->
        <div class="space-y-3 text-sm">
          <div class="flex justify-between py-2 border-b border-gray-bg">
            <span class="text-text-secondary">手机号</span>
            <span class="text-text-primary">{{ userStore.userInfo.phone || '未绑定' }}</span>
          </div>
          <div class="flex justify-between py-2 border-b border-gray-bg">
            <span class="text-text-secondary">注册时间</span>
            <span class="text-text-primary">{{ formatDate(userStore.userInfo.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import { useUserStore } from '../stores/user'
import { formatPrice } from '../utils/format'
const userStore = useUserStore()
const rechargeAmount = ref('')
const recharging = ref(false)
function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}
async function handleRecharge() {
  const amount = Number(rechargeAmount.value)
  if (amount <= 0) {
    window.$toast.error('请输入有效金额')
    return
  }
  recharging.value = true
  try {
    await userStore.recharge(amount)
    window.$toast.success('充值成功')
    rechargeAmount.value = ''
  } catch (e) {
    window.$toast.error(e.message)
  } finally {
    recharging.value = false
  }
}
</script>


