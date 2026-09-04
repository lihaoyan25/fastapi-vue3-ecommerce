<template>
  <div class="flex flex-col items-center justify-center py-20 text-center">
    <div class="text-6xl mb-4">{{ icon }}</div>
    <h3 class="text-lg font-medium text-text-primary mb-2">{{ title }}</h3>
    <p class="text-text-secondary text-sm">{{ description }}</p>
    <slot></slot>
  </div>
</template>

<script setup>
defineProps({
  icon: {
    type: String,
    default: '📭'
  },
  title: {
    type: String,
    default: '暂无数据'
  },
  description: {
    type: String,
    default: ''
  }
})
</script>
