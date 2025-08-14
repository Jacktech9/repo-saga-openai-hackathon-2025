<template>
  <div class="chat-container">
    <div class="chat-dialog" @click.stop>
      <!-- 聊天標題 -->
      <div class="chat-header">
        <div class="chat-title">
          <span class="chat-icon">🧙‍♂️</span>
          <h3>{{ texts.title }}</h3>
        </div>
        <button @click="$emit('close')" class="close-btn">✕</button>
      </div>

      <!-- 聊天記錄區域 -->
      <div class="chat-messages" ref="messagesContainer">
        <div v-if="messages.length === 0" class="welcome-message">
          <div class="welcome-content">
            <span class="welcome-icon">✨</span>
            <p>{{ texts.welcomeTitle }} {{ texts.welcomeSubtitle }}</p>
            <p>{{ texts.welcomeDescription }}</p>
          </div>
        </div>
        
        <div v-for="(message, index) in messages" :key="index" class="message" :class="message.type">
          <div class="message-avatar">
            <span v-if="message.type === 'user'">👤</span>
            <span v-else>🧙‍♂️</span>
          </div>
          <div class="message-content">
            <div class="message-bubble">
              <p>{{ message.content }}</p>
              <span class="message-time">{{ formatTime(message.timestamp) }}</span>
            </div>
          </div>
        </div>

        <!-- 正在輸入指示器 -->
        <div v-if="isTyping" class="message assistant">
          <div class="message-avatar">
            <span>🧙‍♂️</span>
          </div>
          <div class="message-content">
            <div class="message-bubble typing">
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 輸入區域 -->
      <div class="chat-input-area">
        <div class="input-container">
          <input
            v-model="currentMessage"
            @keypress.enter="sendMessage"
            :placeholder="texts.placeholder"
            class="chat-input"
            :disabled="isTyping"
          />
          <button 
            @click="sendMessage" 
            class="send-btn"
            :disabled="!currentMessage.trim() || isTyping"
          >
            <span v-if="!isTyping">🚀</span>
            <span v-else class="loading-spinner-small"></span>
          </button>
        </div>
        <div class="input-hint">
          <span>{{ texts.hint }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, computed } from 'vue'
import { chatWithAssistant } from '../services/api'
import { useI18n } from '../i18n'

// 定義 emit
defineEmits(['close'])

// 語言設定
const { lang } = useI18n()

// 響應式數據
const messages = ref([])
const currentMessage = ref('')
const isTyping = ref(false)
const messagesContainer = ref(null)

// 多語言文字
const texts = computed(() => {
  const isEnglish = lang.value === 'en'

  return {
    title: isEnglish ? 'Repo Saga Assistant' : 'Repo Saga 助手',
    welcomeTitle: isEnglish ? 'Welcome to Repo Saga Engine!' : '歡迎來到 Repo Saga Engine！',
    welcomeSubtitle: isEnglish ? 'I help transform GitHub projects into poetry and fiction.' : '我專門協助將 GitHub 專案轉化為詩歌與小說。',
    welcomeDescription: isEnglish
      ? 'Ask me about repository analysis, literary transformation techniques, or how to improve your generated works.'
      : '你可以問我關於倉庫分析、文學轉化技巧，或如何改善生成的作品。',
    placeholder: isEnglish
      ? 'Ask about repository analysis or literary transformation...'
      : '詢問倉庫分析或文學轉化相關問題...',
    hint: isEnglish
      ? '💡 Try: "How does the analysis work?" or "Tips for better poetry generation" or "Explain the novel creation process"'
      : '💡 試試問：「分析是如何運作的？」或「如何生成更好的詩歌？」或「解釋小說創作流程」',
    errorMessage: isEnglish
      ? 'Sorry, the literary transformation service is temporarily unavailable. Please try again later.'
      : '抱歉，文學轉化服務暫時無法使用，請稍後再試。'
  }
})

// 發送消息
async function sendMessage() {
  if (!currentMessage.value.trim() || isTyping.value) {
    return
  }

  // 添加用戶消息
  const userMessage = {
    type: 'user',
    content: currentMessage.value,
    timestamp: new Date()
  }
  messages.value.push(userMessage)

  const messageToSend = currentMessage.value
  currentMessage.value = ''

  // 滾動到底部
  await nextTick()
  scrollToBottom()

  // 顯示正在輸入
  isTyping.value = true

  try {
    // 準備對話歷史（轉換為 API 需要的格式）
    const conversationHistory = messages.value
      .slice(0, -1) // 排除剛添加的用戶消息
      .map(msg => ({
        role: msg.type === 'user' ? 'user' : 'assistant',
        content: msg.content
      }))

    // 調用真正的 AI API，傳遞語言設定
    const aiResponse = await chatWithAssistant(
      messageToSend,
      conversationHistory,
      lang.value,
      lang.value === 'zh-TW' ? 'zh-TW' : 'en-US'
    )

    // 添加 AI 回應
    const aiMessage = {
      type: 'assistant',
      content: aiResponse,
      timestamp: new Date()
    }
    messages.value.push(aiMessage)

  } catch (error) {
    console.error('Chat API error:', error)

    // 如果 API 調用失敗，顯示友好的錯誤消息
    const errorMessage = {
      type: 'assistant',
      content: texts.value.errorMessage,
      timestamp: new Date()
    }
    messages.value.push(errorMessage)
  } finally {
    isTyping.value = false
    await nextTick()
    scrollToBottom()
  }
}



// 格式化時間
function formatTime(timestamp) {
  return timestamp.toLocaleTimeString('zh-TW', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

// 滾動到底部
function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// 組件掛載時的初始化
onMounted(() => {
  // 可以在這裡添加初始化邏輯
})
</script>

<style scoped>
.chat-container {
  position: fixed;
  bottom: 5rem;
  right: 2rem;
  z-index: 1001;
}

.chat-dialog {
  width: 400px;
  height: 600px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.chat-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.chat-icon {
  font-size: 1.5rem;
}

.chat-title h3 {
  margin: 0;
  font-size: 1.2rem;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background: #f8f9fa;
}

.welcome-message {
  text-align: center;
  padding: 2rem 1rem;
}

.welcome-content {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.welcome-icon {
  font-size: 2rem;
  display: block;
  margin-bottom: 1rem;
}

.welcome-content p {
  margin: 0.5rem 0;
  color: #666;
  line-height: 1.5;
}

.message {
  display: flex;
  margin-bottom: 1rem;
  align-items: flex-start;
  gap: 0.75rem;
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  background: #e9ecef;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.message.user .message-avatar {
  background: #667eea;
  color: white;
}

.message-content {
  flex: 1;
  max-width: 80%;
}

.message-bubble {
  background: white;
  padding: 0.75rem 1rem;
  border-radius: 15px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  position: relative;
}

.message.user .message-bubble {
  background: #667eea;
  color: white;
}

.message-bubble p {
  margin: 0;
  line-height: 1.4;
}

.message-time {
  font-size: 0.75rem;
  opacity: 0.7;
  display: block;
  margin-top: 0.25rem;
}

.typing {
  background: #e9ecef !important;
}

.typing-indicator {
  display: flex;
  gap: 0.25rem;
  align-items: center;
}

.typing-indicator span {
  width: 6px;
  height: 6px;
  background: #999;
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.5;
  }
  30% {
    transform: translateY(-10px);
    opacity: 1;
  }
}

.chat-input-area {
  padding: 1rem 1.5rem;
  background: white;
  border-top: 1px solid #e9ecef;
}

.input-container {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.chat-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid #e9ecef;
  border-radius: 25px;
  outline: none;
  font-size: 0.9rem;
  transition: border-color 0.2s ease;
}

.chat-input:focus {
  border-color: #667eea;
}

.send-btn {
  width: 45px;
  height: 45px;
  border: none;
  background: #667eea;
  color: white;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  transition: all 0.2s ease;
}

.send-btn:hover:not(:disabled) {
  background: #5a6fd8;
  transform: scale(1.05);
}

.send-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
}

.loading-spinner-small {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.input-hint {
  font-size: 0.75rem;
  color: #999;
  text-align: center;
}

/* 響應式設計 */
@media (max-width: 768px) {
  .chat-container {
    bottom: 5rem;
    right: 1rem;
    left: 1rem;
  }

  .chat-dialog {
    width: 100%;
    height: 500px;
    border-radius: 15px;
  }

  .message-content {
    max-width: 85%;
  }
}
</style>
