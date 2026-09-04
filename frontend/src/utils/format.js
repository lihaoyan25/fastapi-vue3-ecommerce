// 价格格式化：保留两位小数，加人民币符号
export function formatPrice(price) {
  return '¥' + Number(price).toFixed(2)
}
