import request from './request'

// 获取购物车
export function getCart() {
  return request.get('/cart')
}

// 添加商品到购物车
export function addToCart(product_id, quantity) {
  return request.post('/cart/items', { product_id, quantity })
}

// 更新购物车数量
export function updateCartItem(product_id, quantity) {
  return request.put(`/cart/items/${product_id}`, { quantity })
}

// 删除购物车商品
export function removeCartItem(product_id) {
  return request.delete(`/cart/items/${product_id}`)
}

// 清空购物车
export function clearCart() {
  return request.delete('/cart/clear')
}

// 结算
export function checkout() {
  return request.post('/cart/checkout')
}
