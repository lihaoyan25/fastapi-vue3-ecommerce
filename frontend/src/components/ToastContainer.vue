<template>
  <div class="fixed top-20 left-1/2 -translate-x-1/2 z-50 flex flex-col gap-3">
    <transition-group name="toast">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="[
          'px-6 py-3 rounded-xl shadow-lg text-sm min-w-[200px] text-center',
          toast.type === 'error' ? 'bg-danger text-white' :
          toast.type === 'success' ? 'bg-green-500 text-white' :
          'bg-text-primary text-white'
        ]"
      >
        {{ toast.message }}
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const toasts = ref([])
let id = 0

function showToast(message, type = 'info', duration = 2500) {
  const toastId = ++id
  toasts.value.push({ id: toastId, message, type })
  setTimeout(() => {
    const index = toasts.value.findIndex(t => t.id === toastId)
    if (index > -1) toasts.value.splice(index, 1)
  }, duration)
}

// 挂载到全局
window.$toast = {
  success: msg => showToast(msg, 'success'),
  error: msg => showToast(msg, 'error'),
  info: msg => showToast(msg, 'info')
}

defineExpose({ showToast })
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}
.toast-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}
.toast-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
