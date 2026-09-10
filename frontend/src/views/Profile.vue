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
            <p class="text-text-secondary text-sm flex items-center gap-2">
              {{ userStore.userInfo.email }}
              <button
                @click="openModal('email')"
                class="text-xs text-primary hover:underline btn-transition"
              >
                修改
              </button>
            </p>
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
              class="flex-1 px-4 py-2.5 rounded-xl border border-border-light input-focus text-sm"
              placeholder="输入充值金额"
            />
            <button
              @click="handleRecharge"
              :disabled="recharging"
              class="px-5 py-2.5 bg-gradient-to-r from-yellow-500 to-amber-600 text-white rounded-xl text-sm btn-transition hover:from-yellow-600 hover:to-amber-700 disabled:opacity-50"
            >
              {{ recharging ? '充值中...' : '充值' }}
            </button>
          </div>
        </div>
        <!-- 其他信息 -->
        <div class="space-y-3 text-sm mb-8">
          <div class="flex justify-between items-center py-2 border-b border-gray-bg">
            <span class="text-text-secondary">手机号</span>
            <span class="flex items-center gap-2">
              <span class="text-text-primary">{{ userStore.userInfo.phone || '未绑定' }}</span>
              <button
                @click="openModal('phone')"
                class="text-xs text-primary hover:underline btn-transition"
              >
                修改
              </button>
            </span>
          </div>
          <div class="flex justify-between py-2 border-b border-gray-bg">
            <span class="text-text-secondary">注册时间</span>
            <span class="text-text-primary">{{ formatDate(userStore.userInfo.created_at) }}</span>
          </div>
        </div>

        <!-- 账号安全设置 -->
        <h3 class="font-medium text-text-primary mb-3 pt-6 border-t border-border-light">账号安全</h3>

        <!-- 修改用户名 -->
        <div class="mb-6">
          <p class="text-sm text-text-secondary mb-2">修改用户名</p>
          <div class="flex gap-3">
            <input
              v-model="usernameForm.username"
              type="text"
              class="flex-1 px-4 py-2.5 rounded-xl border border-border-light input-focus"
              :placeholder="userStore.userInfo.username"
            />
            <button
              @click="handleUpdateUsername"
              :disabled="savingUsername"
              class="px-5 py-2.5 bg-gradient-to-r from-yellow-500 to-amber-600 text-white rounded-xl text-sm btn-transition hover:from-yellow-600 hover:to-amber-700 disabled:opacity-50"
            >
              {{ savingUsername ? '保存中...' : '保存' }}
            </button>
          </div>
        </div>

        <!-- 修改密码入口：左下角高亮小字 -->
        <div class="pt-2">
          <button
            @click="openModal('password')"
            class="text-xs text-primary hover:underline btn-transition"
          >
            修改密码
          </button>
        </div>
      </div>
    </div>

    <!-- 悬浮修改弹窗 -->
    <div
      v-if="activeModal"
      class="fixed inset-0 z-50 flex items-center justify-center px-6 bg-black/40"
      @click.self="closeModal"
    >
      <div class="w-full max-w-sm bg-white rounded-2xl shadow-card p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-medium text-text-primary">{{ modalTitle }}</h3>
          <button @click="closeModal" class="text-text-tertiary hover:text-text-primary btn-transition">✕</button>
        </div>

        <!-- 修改邮箱 -->
        <div v-if="activeModal === 'email'" class="space-y-3">
          <input
            v-model="emailForm.email"
            type="email"
            class="w-full px-4 py-2.5 rounded-xl border border-border-light input-focus"
            placeholder="新邮箱"
          />
          <input
            v-model="emailForm.current_password"
            type="password"
            class="w-full px-4 py-2.5 rounded-xl border border-border-light input-focus"
            placeholder="当前密码"
          />
          <button
            @click="handleUpdateEmail"
            :disabled="savingEmail"
            class="w-full py-2.5 bg-gradient-to-r from-yellow-500 to-amber-600 text-white rounded-xl text-sm btn-transition hover:from-yellow-600 hover:to-amber-700 disabled:opacity-50"
          >
            {{ savingEmail ? '保存中...' : '保存' }}
          </button>
        </div>

        <!-- 修改手机号 -->
        <div v-if="activeModal === 'phone'" class="space-y-3">
          <input
            v-model="phoneForm.phone"
            type="tel"
            class="w-full px-4 py-2.5 rounded-xl border border-border-light input-focus"
            :placeholder="userStore.userInfo.phone || '新手机号'"
          />
          <input
            v-model="phoneForm.current_password"
            type="password"
            class="w-full px-4 py-2.5 rounded-xl border border-border-light input-focus"
            placeholder="当前密码"
          />
          <button
            @click="handleUpdatePhone"
            :disabled="savingPhone"
            class="w-full py-2.5 bg-gradient-to-r from-yellow-500 to-amber-600 text-white rounded-xl text-sm btn-transition hover:from-yellow-600 hover:to-amber-700 disabled:opacity-50"
          >
            {{ savingPhone ? '保存中...' : '保存' }}
          </button>
        </div>

        <!-- 修改密码 -->
        <div v-if="activeModal === 'password'" class="space-y-3">
          <input
            v-model="passwordForm.old_password"
            type="password"
            class="w-full px-4 py-2.5 rounded-xl border border-border-light input-focus"
            placeholder="当前密码"
          />
          <input
            v-model="passwordForm.new_password"
            type="password"
            class="w-full px-4 py-2.5 rounded-xl border border-border-light input-focus"
            placeholder="新密码（8-20位，包含大小写字母和数字）"
          />
          <input
            v-model="passwordForm.confirm_password"
            type="password"
            class="w-full px-4 py-2.5 rounded-xl border border-border-light input-focus"
            placeholder="确认新密码"
          />
          <button
            @click="handleChangePassword"
            :disabled="savingPassword"
            class="w-full py-2.5 bg-gradient-to-r from-yellow-500 to-amber-600 text-white rounded-xl text-sm btn-transition hover:from-yellow-600 hover:to-amber-700 disabled:opacity-50"
          >
            {{ savingPassword ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { reactive, ref, computed } from 'vue'
import { useUserStore } from '../stores/user'
import { formatPrice } from '../utils/format'
const userStore = useUserStore()
const rechargeAmount = ref('')
const recharging = ref(false)

// 弹窗状态：email / phone / password
const activeModal = ref(null)
const modalTitle = computed(() => ({
  email: '修改邮箱',
  phone: '修改手机号',
  password: '修改密码'
}[activeModal.value] || ''))

function openModal(type) {
  activeModal.value = type
}
function closeModal() {
  activeModal.value = null
  emailForm.email = ''
  emailForm.current_password = ''
  phoneForm.phone = ''
  phoneForm.current_password = ''
  passwordForm.old_password = ''
  passwordForm.new_password = ''
  passwordForm.confirm_password = ''
}

const usernameForm = reactive({ username: '' })
const emailForm = reactive({ email: '', current_password: '' })
const phoneForm = reactive({ phone: '', current_password: '' })
const passwordForm = reactive({ old_password: '', new_password: '', confirm_password: '' })
const savingUsername = ref(false)
const savingEmail = ref(false)
const savingPhone = ref(false)
const savingPassword = ref(false)

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

async function handleUpdateUsername() {
  if (!usernameForm.username.trim()) {
    window.$toast.error('请输入新用户名')
    return
  }
  savingUsername.value = true
  try {
    await userStore.updateProfile({ username: usernameForm.username.trim() })
    window.$toast.success('用户名修改成功')
    usernameForm.username = ''
  } catch (e) {
    window.$toast.error(e.message)
  } finally {
    savingUsername.value = false
  }
}

async function handleUpdateEmail() {
  if (!emailForm.email.trim()) {
    window.$toast.error('请输入新邮箱')
    return
  }
  if (!emailForm.current_password) {
    window.$toast.error('请输入当前密码')
    return
  }
  savingEmail.value = true
  try {
    await userStore.updateProfile({
      email: emailForm.email.trim(),
      current_password: emailForm.current_password
    })
    window.$toast.success('邮箱修改成功')
    closeModal()
  } catch (e) {
    window.$toast.error(e.message)
  } finally {
    savingEmail.value = false
  }
}

async function handleUpdatePhone() {
  if (!phoneForm.phone.trim()) {
    window.$toast.error('请输入新手机号')
    return
  }
  if (!phoneForm.current_password) {
    window.$toast.error('请输入当前密码')
    return
  }
  savingPhone.value = true
  try {
    await userStore.updateProfile({
      phone: phoneForm.phone.trim(),
      current_password: phoneForm.current_password
    })
    window.$toast.success('手机号修改成功')
    closeModal()
  } catch (e) {
    window.$toast.error(e.message)
  } finally {
    savingPhone.value = false
  }
}

async function handleChangePassword() {
  if (!passwordForm.old_password || !passwordForm.new_password) {
    window.$toast.error('请填写完整的密码信息')
    return
  }
  if (passwordForm.new_password !== passwordForm.confirm_password) {
    window.$toast.error('两次密码输入不一致')
    return
  }
  savingPassword.value = true
  try {
    await userStore.changePassword(passwordForm.old_password, passwordForm.new_password)
    window.$toast.success('密码修改成功')
    closeModal()
  } catch (e) {
    window.$toast.error(e.message)
  } finally {
    savingPassword.value = false
  }
}
</script>
