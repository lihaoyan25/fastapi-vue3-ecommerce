import { defineStore } from 'pinia'
import {
  createSession, listSessions, getSessionMessages,
  deleteSession, getRecommendations, streamChatMessage
} from '../api/chat'
import { useCartStore } from './cart'

export const useChatStore = defineStore('chat', {
  state: () => ({
    open: false,              // 面板展开状态
    loaded: false,            // 是否已完成首次初始化
    sessions: [],             // 会话列表
    currentSessionId: null,   // 当前会话
    messages: [],             // 当前会话消息 [{role, content, context, streaming, toolStatus}]
    recommendations: { orders: [], products: [], carts: [] },
    sending: false            // 是否正在流式接收回复
  }),

  getters: {
    isEmpty: state => state.messages.length === 0
  },

  actions: {
    /** 首次展开时初始化：恢复最近会话（无则新建）并拉取推荐卡片 */
    async ensureInit() {
      if (this.loaded) return
      this.loaded = true
      try {
        await this.loadSessions()
        if (this.sessions.length === 0) {
          await this.newSession()
        } else {
          await this.switchSession(this.sessions[0].session_id)
        }
      } catch (e) {
        this.loaded = false
        throw e
      }
      this.loadRecommendations().catch(e => {
        console.error('[客服] 推荐卡片加载失败:', e)
      })
    },

    async loadSessions() {
      this.sessions = await listSessions()
    },

    async newSession() {
      const session = await createSession()
      this.sessions.unshift(session)
      await this.switchSession(session.session_id)
    },

    async switchSession(sessionId) {
      if (this.sending) return
      this.currentSessionId = sessionId
      const res = await getSessionMessages(sessionId)
      this.messages = res.messages
    },

    async removeSession(sessionId) {
      await deleteSession(sessionId)
      this.sessions = this.sessions.filter(s => s.session_id !== sessionId)
      if (this.currentSessionId === sessionId) {
        if (this.sessions.length > 0) {
          await this.switchSession(this.sessions[0].session_id)
        } else {
          await this.newSession()
        }
      }
    },

    async loadRecommendations() {
      this.recommendations = await getRecommendations()
    },

    /** 发送消息并流式接收回复 */
    async send(content, context) {
      if (!this.currentSessionId || this.sending) return
      this.sending = true

      // 先落本地：用户消息 + 助手占位气泡
      this.messages.push({ role: 'user', content, context: context ? { ...context } : null })
      // 从响应式数组中取代理引用，流式追加内容才能触发视图更新
      this.messages.push({ role: 'assistant', content: '', streaming: true, toolStatus: '' })
      const assistantMsg = this.messages[this.messages.length - 1]

      try {
        await streamChatMessage({
          sessionId: this.currentSessionId,
          content,
          context,
          onEvent: ev => {
            if (ev.type === 'delta') {
              assistantMsg.content += ev.content
            } else if (ev.type === 'tool') {
              assistantMsg.toolStatus = ev.display
            } else if (ev.type === 'done') {
              assistantMsg.streaming = false
              assistantMsg.toolStatus = ''
            } else if (ev.type === 'error') {
              throw { message: ev.message }
            }
          }
        })
        // 流正常结束但未收到 done（异常截断）时兜底收尾
        assistantMsg.streaming = false
        assistantMsg.toolStatus = ''
      } catch (e) {
        assistantMsg.streaming = false
        assistantMsg.toolStatus = ''
        // 无任何回复内容时移除占位气泡
        if (!assistantMsg.content) this.messages.pop()
        throw e
      } finally {
        this.sending = false
        // 工具可能改动了购物车/订单，静默刷新推荐与购物车角标
        this.loadRecommendations().catch(() => {})
        useCartStore().refreshCart().catch(() => {})
      }
    }
  }
})
