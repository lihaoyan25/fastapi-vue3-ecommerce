import request from './request'

// 获取商品列表
export function getProducts(params = {}) {
  return request.get('/products', { params })
}

// 获取商品详情
export function getProductDetail(id) {
  return request.get(`/products/${id}`)
}

// 搜索商品
export function searchProducts(keyword, params = {}) {
  return request.get('/products/search', {
    params: { keyword, ...params }
  })
}

// 管理员创建商品
export function createProduct(data) {
  return request.post('/products', data)
}

// 管理员更新商品
export function updateProduct(id, data) {
  return request.put(`/products/${id}`, data)
}

// 管理员删除商品
export function deleteProduct(id) {
  return request.delete(`/products/${id}`)
}
