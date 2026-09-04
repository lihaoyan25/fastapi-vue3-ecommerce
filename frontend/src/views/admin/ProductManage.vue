<template>
  <!-- 灰金奢华渐变背景外层容器 -->
  <div class="gradient-bg min-h-screen">
    <div class="max-w-6xl mx-auto px-6 py-10">
      <div class="flex items-center justify-between mb-8">
        <h1 class="text-2xl font-semibold text-text-primary">商品管理</h1>
        <button
          @click="openCreateModal"
          class="px-5 py-2.5 bg-gradient-to-r from-yellow-500 to-amber-600 text-white rounded-xl btn-transition hover:from-yellow-600 hover:to-amber-700"
        >
          + 新增商品
        </button>
      </div>
      <!-- 商品列表 -->
      <div class="bg-white rounded-2xl shadow-card overflow-hidden">
        <table class="w-full">
          <thead class="bg-gray-bg text-text-secondary text-sm">
            <tr>
              <th class="text-left px-6 py-3 font-medium">ID</th>
              <th class="text-left px-6 py-3 font-medium">商品名称</th>
              <th class="text-left px-6 py-3 font-medium">价格</th>
              <th class="text-left px-6 py-3 font-medium">库存</th>
              <th class="text-left px-6 py-3 font-medium">状态</th>
              <th class="text-right px-6 py-3 font-medium">操作</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-bg">
            <tr v-for="item in products" :key="item.product_id" class="hover:bg-gray-bg/50 transition-colors">
              <td class="px-6 py-4 text-text-primary">{{ item.product_id }}</td>
              <td class="px-6 py-4 text-text-primary font-medium">{{ item.name }}</td>
              <td class="px-6 py-4 text-text-primary">{{ formatPrice(item.price) }}</td>
              <td class="px-6 py-4 text-text-primary">{{ item.stock }}</td>
              <td class="px-6 py-4">
                <span
                  :class="[
                    'px-2 py-0.5 rounded-full text-xs',
                    item.is_active ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-500'
                  ]"
                >
                  {{ item.is_active ? '上架中' : '已下架' }}
                </span>
              </td>
              <td class="px-6 py-4 text-right">
                <button
                  @click="handleEdit(item)"
                  class="text-primary hover:underline mr-4 text-sm btn-transition"
                >
                  编辑
                </button>
                <button
                  @click="handleDelete(item.product_id)"
                  class="text-danger hover:underline text-sm btn-transition"
                >
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!-- 新增/编辑弹窗 -->
      <transition name="modal">
        <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-6">
          <div class="absolute inset-0 bg-black/30 backdrop-blur-sm" @click="closeModal"></div>
          <div class="relative bg-white rounded-2xl shadow-xl w-full max-w-md p-6">
            <h2 class="text-xl font-semibold text-text-primary mb-6">
              {{ editingId ? '编辑商品' : '新增商品' }}
            </h2>
            <form @submit.prevent="handleSubmit" class="space-y-4">
              <div>
                <label class="block text-sm text-text-secondary mb-1.5">商品名称</label>
                <input
                  v-model="form.name"
                  type="text"
                  class="w-full px-4 py-2.5 rounded-xl border border-border-light input-focus"
                  required
                />
              </div>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm text-text-secondary mb-1.5">价格</label>
                  <input
                    v-model.number="form.price"
                    type="number"
                    step="0.01"
                    min="0.01"
                    class="w-full px-4 py-2.5 rounded-xl border border-border-light input-focus"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm text-text-secondary mb-1.5">库存</label>
                  <input
                    v-model.number="form.stock"
                    type="number"
                    min="0"
                    class="w-full px-4 py-2.5 rounded-xl border border-border-light input-focus"
                    required
                  />
                </div>
              </div>
              <div>
                <label class="block text-sm text-text-secondary mb-1.5">商品描述</label>
                <textarea
                  v-model="form.description"
                  rows="3"
                  class="w-full px-4 py-2.5 rounded-xl border border-border-light input-focus resize-none"
                ></textarea>
              </div>
              <div>
                <label class="block text-sm text-text-secondary mb-1.5">图片链接</label>
                <input
                  v-model="form.image_url"
                  type="text"
                  class="w-full px-4 py-2.5 rounded-xl border border-border-light input-focus"
                  placeholder="/static/upload/<filename...>"
                />
              </div>
              <div class="flex gap-3 pt-4">
                <button
                  type="button"
                  @click="closeModal"
                  class="flex-1 py-2.5 border border-border-light rounded-xl text-text-secondary btn-transition hover:bg-gray-bg"
                >
                  取消
                </button>
                <button
                  type="submit"
                  :disabled="submitting"
                  class="flex-1 py-2.5 bg-gradient-to-r from-yellow-500 to-amber-600 text-white rounded-xl btn-transition hover:from-yellow-600 hover:to-amber-700 disabled:opacity-50"
                >
                  {{ submitting ? '保存中...' : '保存' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>
<script setup>
import { ref, reactive, watch, onMounted } from 'vue'
import { getProducts, createProduct, updateProduct, deleteProduct } from '../../api/product'
import { formatPrice } from '../../utils/format'
const products = ref([])
const showModal = ref(false)
const editingId = ref(null)
const submitting = ref(false)
const form = reactive({
  name: '',
  price: '',
  stock: '',
  description: '',
  image_url: ''
})
async function loadProducts() {
  try {
    const res = await getProducts({ page: 1, page_size: 100 })
    products.value = res.items
  } catch (e) {
    window.$toast.error(e.message)
  }
}
function openCreateModal() {
  editingId.value = null
  resetForm()
  showModal.value = true
}
function handleEdit(item) {
  editingId.value = item.product_id
  form.name = item.name
  form.price = item.price
  form.stock = item.stock
  form.description = item.description || ''
  form.image_url = item.image_url || ''
  showModal.value = true
}
function closeModal() {
  showModal.value = false
}
function resetForm() {
  form.name = ''
  form.price = ''
  form.stock = ''
  form.description = ''
  form.image_url = ''
}
async function handleSubmit() {
  submitting.value = true
  try {
    if (editingId.value) {
      await updateProduct(editingId.value, form)
      window.$toast.success('更新成功')
    } else {
      await createProduct(form)
      window.$toast.success('创建成功')
    }
    closeModal()
    loadProducts()
  } catch (e) {
    window.$toast.error(e.message)
  } finally {
    submitting.value = false
  }
}
async function handleDelete(id) {
  if (!confirm('确定要删除该商品吗？删除后将下架。')) return
  try {
    await deleteProduct(id)
    window.$toast.success('已删除')
    loadProducts()
  } catch (e) {
    window.$toast.error(e.message)
  }
}
watch(showModal, val => {
  if (!val) resetForm()
})
onMounted(() => {
  loadProducts()
})
</script>
<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: all 0.25s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-from > div:last-child,
.modal-leave-to > div:last-child {
  transform: scale(0.95) translateY(10px);
}
</style>
