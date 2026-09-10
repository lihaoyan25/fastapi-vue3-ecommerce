import request from './request'

// 注册
export function register(data) {
  return request.post('/auth/register', data)
}

// 登录
export function login(username, password) {
  const form = new URLSearchParams()
  form.append('username', username)
  form.append('password', password)
  return request.post('/auth/login', form, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  })
}

// 获取当前用户信息
export function getCurrentUser() {
  return request.get('/auth/me')
}

// 忘记密码：账号(用户名或邮箱)+手机号验证身份后重置
export function forgotPassword(data) {
  return request.post('/auth/forgot-password', data)
}
