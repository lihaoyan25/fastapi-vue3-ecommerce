import request from './request'

// 创建订单（购物车选中商品结算）
export function createOrder(product_ids) {
  return request.post('/orders', { product_ids })
}

// 获取订单列表
export function getOrders(page = 1, page_size = 10, status = null) {
  return request.get('/orders', { params: { page, page_size, status } })
}

// 获取订单详情
export function getOrder(order_id) {
  return request.get(`/orders/${order_id}`)
}

// 支付订单
export function payOrder(order_id) {
  return request.post(`/orders/${order_id}/pay`)
}

// 取消订单
export function cancelOrder(order_id) {
  return request.post(`/orders/${order_id}/cancel`)
}

// 删除订单
export function deleteOrder(order_id) {
  return request.delete(`/orders/${order_id}`)
}
