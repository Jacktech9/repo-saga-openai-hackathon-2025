import axios from 'axios'

// 優先使用環境變數，否則預設為本機開發端點
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000, // 120秒超時（AI 生成需要較長時間）
})

export const generateWork = async (url, presets = {}) => {
  try {
    const payload = { url, ...presets }
    const response = await api.post('/generate', payload)
    return response.data
  } catch (error) {
    console.error('API call failed:', error)
    throw error
  }
}

export const getExample = async () => {
  try {
    const response = await api.get('/example')
    return response.data
  } catch (error) {
    console.error('Failed to get example:', error)
    throw error
  }
}

export const chatWithAssistant = async (message, conversationHistory = [], lang = null, locale = null) => {
  try {
    const response = await api.post('/chat', {
      message,
      conversation_history: conversationHistory,
      lang,
      locale
    })
    return response.data.response
  } catch (error) {
    console.error('Chat API call failed:', error)
    throw error
  }
}
