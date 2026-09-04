<template>
  <!-- 外层渐变背景容器 -->
  <div class="gradient-bg min-h-screen">
    <div class="max-w-6xl mx-auto px-6 py-10">
      <!-- 搜索栏 -->
      <div class="mb-8">
        <div class="max-w-xl mx-auto relative">
          <input
            v-model="keyword"
            type="text"
            @keyup.enter="handleSearch"
            class="w-full pl-12 pr-4 py-3 rounded-full border border-border-light bg-white input-focus text-text-primary"
            placeholder="搜索商品..."
          />
          <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>
      <!-- 商品网格 -->
      <div v-if="products.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <ProductCard v-for="product in products" :key="product.product_id" :product="product" />
      </div>
      <!-- 空状态 -->
      <EmptyState
        v-else-if="!loading"
        icon="🔍"
        title="未找到相关商品"
        description="换个关键词试试吧"
      />
      <!-- 加载更多 -->
      <div v-if="hasMore && !loading" class="text-center mt-12">
        <button
          @click="loadMore"
          class="px-8 py-2.5 bg-white border border-border-light rounded-full text-text-secondary hover:text-primary hover:border-primary btn-transition"
        >
          加载更多
        </button>
      </div>
      <div v-if="loading" class="text-center py-12 text-text-secondary">
        加载中...
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, onMounted } from 'vue'
import ProductCard from '../components/ProductCard.vue'
import EmptyState from '../components/EmptyState.vue'
import { getProducts, searchProducts } from '../api/product'
const products = ref([])
const keyword = ref('')
const page = ref(1)
const pageSize = 12
const total = ref(0)
const loading = ref(false)
const hasMore = computed(() => products.value.length < total.value)
async function loadProducts() {
  loading.value = true
  try {
    const res = keyword.value
      ? await searchProducts(keyword.value, { page: page.value, page_size: pageSize })
      : await getProducts({ page: page.value, page_size: pageSize })
    
    if (page.value === 1) {
      products.value = res.items
    } else {
      products.value = [...products.value, ...res.items]
    }
    total.value = res.total
  } catch (e) {
    window.$toast.error(e.message)
  } finally {
    loading.value = false
  }
}
function handleSearch() {
  page.value = 1
  products.value = []
  loadProducts()
}
function loadMore() {
  page.value++
  loadProducts()
}
onMounted(() => {
  loadProducts()
})
</script>


