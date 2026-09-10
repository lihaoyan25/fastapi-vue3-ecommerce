import request from './request'

// 新建客服会话
export function createSession() {
  return request.post('/chat/sessions')
}

// 会话列表
export function listSessions() {
  return request.get('/chat/sessions')
}

// 会话消息历史
export function getSessionMessages(sessionId) {
  return request.get(`/chat/sessions/${sessionId}/messages`)
}

// 删除会话
export function deleteSession(sessionId) {
  return request.delete(`/chat/sessions/${sessionId}`)
}

// 推荐卡片（最近订单/在售商品/购物车项）
export function getRecommendations() {
  return request.get('/chat/recommendations')
}

/**
 * 流式对话（SSE）。
 * POST 请求无法使用 EventSource，这里用 fetch + ReadableStream 手动解析。
 * 事件格式见后端 routes/chat.py：meta / delta / tool / done / error
 */
export async function streamChatMessage({ sessionId, content, context, signal, onEvent }) {
  const token = localStorage.getItem('token')
  const resp = await fetch(`/api/v1/chat/sessions/${sessionId}/messages/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    },
    body: JSON.stringify({ content, ...(context ? { context } : {}) }),
    signal
  })

  if (!resp.ok || !resp.body) {
    const messageMap = { 401: '登录已过期，请重新登录', 403: '您没有权限使用智能客服', 503: '智能客服功能未启用' }
    throw { status: resp.status, message: messageMap[resp.status] || '客服服务异常，请稍后再试' }
  }

  const reader = resp.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    // SSE 事件以空行分隔
    const parts = buffer.split('\n\n')
    buffer = parts.pop() || ''
    for (const part of parts) {
      const line = part.trim()
      if (!line.startsWith('data:')) continue
      try {
        onEvent(JSON.parse(line.slice(5).trim()))
      } catch {
        // 忽略无法解析的事件片段
      }
    }
  }
}
