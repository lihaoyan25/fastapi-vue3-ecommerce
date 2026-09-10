import { defineStore } from 'pinia'
import { login, register, getCurrentUser } from '../api/auth'
import request from '../api/request'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: null
  }),

  getters: {
    isLoggedIn: state => !!state.token,
    isAdmin: state => state.userInfo?.role === 'admin'
  },

  actions: {
    // 登录
    async login(username, password) {
      const res = await login(username, password)
      this.token = res.access_token
      localStorage.setItem('token', res.access_token)
      localStorage.setItem('refresh_token', res.refresh_token)
      await this.fetchUserInfo()
      return res
    },

    // 注册
    async register(data) {
      return await register(data)
    },

    // 获取用户信息
    async fetchUserInfo() {
      if (!this.token) return null
      try {
        const res = await getCurrentUser()
        this.userInfo = res
        return res
      } catch (e) {
        this.logout()
        throw e
      }
    },

    // 充值
    async recharge(amount) {
      const res = await request.post('/users/me/recharge', { amount })
      this.userInfo.balance = res.balance
      return res
    },

    // 更新个人资料（用户名/邮箱/手机号）
    async updateProfile(data) {
      const res = await request.put('/users/me', data)
      this.userInfo = res
      return res
    },

    // 修改密码
    async changePassword(oldPassword, newPassword) {
      return await request.put('/users/me/password', {
        old_password: oldPassword,
        new_password: newPassword
      })
    },

    // 登出
    logout() {
      this.token = ''
      this.userInfo = null
      localStorage.removeItem('token')
      localStorage.removeItem('refresh_token')
    }
  }
})
