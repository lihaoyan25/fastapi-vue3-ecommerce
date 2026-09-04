<template>
  <!-- 灰金奢华渐变背景外层容器 -->
  <div class="gradient-bg min-h-screen">
    <div class="max-w-5xl mx-auto px-6 py-12">
      <div v-if="product" class="grid grid-cols-1 md:grid-cols-2 gap-12">
        <!-- 商品图 -->
        <div class="aspect-square rounded-2xl bg-white shadow-card flex items-center justify-center overflow-hidden">
          <img
            v-if="product.image_url"
            :src="product.image_url"
            :alt="product.name"
            class="w-full h-full object-cover"
          />
          <span v-else class="text-8xl">📦</span>
        </div>
        <!-- 商品信息 -->
        <div class="flex flex-col">
          <h1 class="text-3xl font-semibold text-text-primary mb-3">{{ product.name }}</h1>
          <p class="text-2xl font-bold text-text-primary mb-6">{{ formatPrice(product.price) }}</p>
          
          <p class="text-text-secondary mb-8 leading-relaxed" style="white-space: pre-line;">
            {{ product.description || '暂无商品描述' }}
          </p>
          <div class="flex items-center gap-4 mb-8">
            <span class="text-sm text-text-secondary">库存：{{ product.stock }} 件</span>
          </div>
          <!-- 数量选择 -->
          <div class="flex items-center gap-4 mb-8">
            <span class="text-sm text-text-secondary">数量</span>
            <div class="flex items-center border border-border-light rounded-xl">
              <button
                @click="quantity = Math.max(1, quantity - 1)"
                class="w-10 h-10 flex items-center justify-center text-text-secondary hover:text-primary btn-transition"
              >
                −
              </button>
              <span class="w-12 text-center">{{ quantity }}</span>
              <button
                @click="quantity = Math.min(product.stock, quantity + 1)"
                class="w-10 h-10 flex items-center justify-center text-text-secondary hover:text-primary btn-transition"
              >
                +
              </button>
            </div>
          </div>
          <!-- 操作按钮 → 香槟金渐变，全站统一 -->
          <div class="flex gap-4">
            <button
              @click="handleAddToCart"
              :disabled="adding || product.stock === 0"
              class="flex-1 bg-gradient-to-r from-yellow-500 to-amber-600 text-white py-3.5 rounded-xl font-medium btn-transition hover:from-yellow-600 hover:to-amber-700 disabled:opacity-50"
            >
              {{ adding ? '添加中...' : '加入购物车' }}
            </button>
          </div>
        </div>
      </div>
      <!-- 加载中 / 错误 -->
      <div v-if="loading" class="text-center py-20 text-text-secondary">加载中...</div>
      <EmptyState
        v-else-if="error"
        icon="❓"
        :title="error"
        description="商品可能已下架或不存在"
      >
        <router-link to="/" class="inline-block mt-6 px-6 py-2 bg-gradient-to-r from-yellow-500 to-amber-600 text-white rounded-full btn-transition hover:from-yellow-600 hover:to-amber-700">
          返回首页
        </router-link>
      </EmptyState>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getProductDetail } from '../api/product'
import { useCartStore } from '../stores/cart'
import { formatPrice } from '../utils/format'
import EmptyState from '../components/EmptyState.vue'
const route = useRoute()
const cartStore = useCartStore()
const product = ref(null)
const quantity = ref(1)
const loading = ref(true)
const adding = ref(false)
const error = ref('')
async function loadProduct() {
  loading.value = true
  error.value = ''
  try {
    product.value = await getProductDetail(route.params.id)
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
async function handleAddToCart() {
  adding.value = true
  try {
    await cartStore.addItem(product.value.product_id, quantity.value)
    window.$toast.success('已加入购物车')
  } catch (e) {
    window.$toast.error(e.message)
  } finally {
    adding.value = false
  }
}
onMounted(() => {
  loadProduct()
})
</script>


