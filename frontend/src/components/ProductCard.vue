<template>
  <router-link
    :to="`/product/${product.product_id}`"
    class="block bg-white rounded-2xl p-5 shadow-card hover:shadow-card-hover transition-all duration-300 ease-apple hover:-translate-y-1 group"
  >
    <!-- 商品图 -->
    <div class="aspect-square rounded-xl bg-gray-bg mb-4 flex items-center justify-center overflow-hidden">
      <img
        v-if="product.image_url"
        :src="product.image_url"
        :alt="product.name"
        class="w-full h-full object-cover"
      />
      <span v-else class="text-5xl">📦</span>
    </div>

    <h3 class="font-medium text-text-primary mb-1 truncate group-hover:text-primary transition-colors">
      {{ product.name }}
    </h3>
    <p class="text-text-secondary text-sm mb-3 line-clamp-2 h-10">
      {{ product.description || '暂无描述' }}
    </p>
    <p class="text-lg font-semibold text-text-primary">
      {{ formatPrice(product.price) }}
    </p>
  </router-link>
</template>

<script setup>
import { formatPrice } from '../utils/format'

defineProps({
  product: {
    type: Object,
    required: true
  }
})
</script>
