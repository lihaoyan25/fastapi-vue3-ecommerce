import { defineStore } from 'pinia'
import { getCart, addToCart, updateCartItem, removeCartItem, checkout } from '../api/cart'

export const useCartStore = defineStore('cart', {
  state: () => ({
    cartData: null
  }),

  getters: {
    totalQuantity: state => state.cartData?.total_quantity || 0,
    totalAmount: state => state.cartData?.total_amount || 0,
    items: state => state.cartData?.items || []
  },

  actions: {
    // 刷新购物车
    async refreshCart() {
      const res = await getCart()
      this.cartData = res
      return res
    },

    // 添加商品
    async addItem(product_id, quantity = 1) {
      const res = await addToCart(product_id, quantity)
      this.cartData = res
      return res
    },

    // 更新数量
    async updateQuantity(product_id, quantity) {
      const res = await updateCartItem(product_id, quantity)
      this.cartData = res
      return res
    },

    // 删除商品
    async removeItem(product_id) {
      const res = await removeCartItem(product_id)
      this.cartData = res
      return res
    },

    // 结算
    async checkout() {
      const res = await checkout()
      this.cartData = { items: [], total_amount: 0, total_quantity: 0 }
      return res
    }
  }
})
