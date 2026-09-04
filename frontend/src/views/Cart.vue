<template>
  <!-- 灰金奢华渐变背景外层容器 -->
  <div class="gradient-bg min-h-screen">
    <div class="max-w-4xl mx-auto px-6 py-10">
      <h1 class="text-2xl font-semibold text-text-primary mb-8">购物车</h1>
      <div v-if="cartStore.items.length > 0" class="flex gap-8">
        <!-- 商品列表 -->
        <div class="flex-1 space-y-4">
          <div
            v-for="item in cartStore.items"
            :key="item.cart_item_id"
            class="bg-white rounded-xl p-5 shadow-card flex items-center gap-5"
          >
          <!-- 商品图 -->
          <div class="w-20 h-20 rounded-lg bg-gray-bg flex items-center justify-center flex-shrink-0 overflow-hidden">
            <img
              v-if="item.image_url"
              :src="item.image_url"
              alt=""
              class="w-full h-full object-cover"
            />
            <span v-else class="text-3xl">📦</span>
          </div>
            <!-- 信息 -->
            <div class="flex-1 min-w-0">
              <h3 class="font-medium text-text-primary truncate">{{ item.product_name }}</h3>
              <p class="text-primary font-semibold mt-1">{{ formatPrice(item.product_price) }}</p>
            </div>
            <!-- 数量控制 -->
            <div class="flex items-center border border-border-light rounded-lg">
              <button
                @click="updateQuantity(item.product_id, item.quantity - 1)"
                class="w-8 h-8 flex items-center justify-center text-text-secondary hover:text-primary btn-transition"
              >
                −
              </button>
              <span class="w-10 text-center text-sm">{{ item.quantity }}</span>
              <button
                @click="updateQuantity(item.product_id, item.quantity + 1)"
                class="w-8 h-8 flex items-center justify-center text-text-secondary hover:text-primary btn-transition"
              >
                +
              </button>
            </div>
            <!-- 小计 -->
            <div class="text-right w-24">
              <p class="font-semibold text-text-primary">{{ formatPrice(item.subtotal) }}</p>
            </div>
            <!-- 删除 -->
            <button
              @click="removeItem(item.product_id)"
              class="text-text-tertiary hover:text-danger btn-transition"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
        <!-- 结算栏 -->
        <div class="w-72 flex-shrink-0">
          <div class="bg-white rounded-xl p-6 shadow-card sticky top-24">
            <div class="flex justify-between mb-3 text-text-secondary">
              <span>商品数量</span>
              <span>{{ cartStore.totalQuantity }} 件</span>
            </div>
            <div class="flex justify-between mb-6 text-lg font-semibold text-text-primary">
              <span>合计</span>
              <span>{{ formatPrice(cartStore.totalAmount) }}</span>
            </div>
            <button
              @click="handleCheckout"
              :disabled="checkingOut"
              class="w-full bg-gradient-to-r from-yellow-500 to-amber-600 text-white py-3 rounded-xl font-medium btn-transition hover:from-yellow-600 hover:to-amber-700 disabled:opacity-50"
            >
              {{ checkingOut ? '结算中...' : '立即结算' }}
            </button>
            <button
              @click="handleClear"
              class="w-full mt-3 text-sm text-text-secondary hover:text-danger btn-transition"
            >
              清空购物车
            </button>
          </div>
        </div>
      </div>
      <!-- 空购物车 -->
      <EmptyState
        v-else
        icon="🛒"
        title="购物车是空的"
        description="快去挑选心仪的商品吧"
      >
        <router-link to="/" class="inline-block mt-6 px-6 py-2 bg-gradient-to-r from-yellow-500 to-amber-600 text-white rounded-full btn-transition hover:from-yellow-600 hover:to-amber-700">
          去逛逛
        </router-link>
      </EmptyState>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useCartStore } from '../stores/cart'
import { formatPrice } from '../utils/format'
import EmptyState from '../components/EmptyState.vue'
import { clearCart } from '../api/cart'
const cartStore = useCartStore()
const checkingOut = ref(false)
async function updateQuantity(product_id, quantity) {
  if (quantity < 1) {
    removeItem(product_id)
    return
  }
  try {
    await cartStore.updateQuantity(product_id, quantity)
  } catch (e) {
    window.$toast.error(e.message)
  }
}
async function removeItem(product_id) {
  try {
    await cartStore.removeItem(product_id)
    window.$toast.success('已移除商品')
  } catch (e) {
    window.$toast.error(e.message)
  }
}
async function handleClear() {
  if (!confirm('确定要清空购物车吗？')) return
  try {
    await clearCart()
    await cartStore.refreshCart()
    window.$toast.success('购物车已清空')
  } catch (e) {
    window.$toast.error(e.message)
  }
}
async function handleCheckout() {
  checkingOut.value = true
  try {
    const res = await cartStore.checkout()
    window.$toast.success(`结算成功，共消费 ${formatPrice(res.total_amount)}`)
  } catch (e) {
    window.$toast.error(e.message)
  } finally {
    checkingOut.value = false
  }
}
onMounted(() => {
  cartStore.refreshCart().catch(e => {
    window.$toast.error(e.message)
  })
})
</script>


