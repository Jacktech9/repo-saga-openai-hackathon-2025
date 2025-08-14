<template>
  <div id="app">
    <header class="app-header">
      <div class="header-content">
        <h1 class="app-title">
          <span class="title-icon">🎭</span>
          Repo Saga Engine
        </h1>
        <p class="app-subtitle">{{ t('app.subtitle') }}</p>
      </div>
    <LanguageSwitcher />
    </header>

    <main class="main-content">
      <!-- 統一的結果展示槽，保持位置不變 -->
      <section class="results-slot">
        <div v-if="isLoading" class="loading-section">
          <div class="loading-animation">
            <div class="loading-spinner"></div>
            <h3>🎨 {{ t('input.generating') }}</h3>
            <p>{{ t('example.desc') }}</p>
          </div>
        </div>
        <template v-else>
          <div v-if="currentWork" class="example-section">
            <ResultsDisplay :work="currentWork" />
            <div class="divider"></div>
          </div>
          <div v-else class="example-section">
            <div class="example-header">
              <h2>✨ {{ t('example.title') }}</h2>
              <p>{{ t('example.desc') }}</p>
            </div>
            <ResultsDisplay :work="fastapiExample" />
            <div class="divider"></div>
          </div>
        </template>
      </section>

      <!-- 輸入區域 -->
      <RepoInput @submit="handleRepoSubmit" :is-loading="isLoading" />



      <!-- 錯誤訊息 -->
      <div v-if="error" class="error-section">
        <div class="error-content">
          <h3>😅 出現了一些問題</h3>
          <p>{{ error }}</p>
          <button @click="clearError" class="retry-btn">重試</button>
        </div>
      </div>


    </main>

    <footer class="app-footer">
      <p>
        Made with ❤️ for OpenAI Open Model Hackathon |
        <a href="https://github.com" target="_blank">GitHub</a>
      </p>

    </footer>

    <!-- 聊天按鈕 -->
    <button @click="toggleChat" class="chat-toggle-btn" :class="{ active: isChatOpen }">
      <span v-if="!isChatOpen">🧙‍♂️</span>
      <span v-else>✕</span>
    </button>

    <!-- 聊天對話框 -->
    <ChatDialog v-if="isChatOpen" @close="toggleChat" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import RepoInput from './components/RepoInput.vue'
import ResultsDisplay from './components/ResultsDisplay.vue'
import ChatDialog from './components/ChatDialog.vue'
import LanguageSwitcher from './components/LanguageSwitcher.vue'
import { useI18n } from './i18n'
import { generateWork } from './services/api'

const isLoading = ref(false)
const currentWork = ref(null)
const error = ref(null)
const isChatOpen = ref(false)
const { t, lang } = useI18n()

// FastAPI example content (auto switches with language)
const fastapiExample = computed(() => {
  if (lang.value === 'en') {
    return {
      repo_url: 'https://github.com/tiangolo/fastapi',
      insight_report: `FastAPI is a modern, high‑performance Python web framework for building APIs.

Key features:
- Blistering performance: comparable to Node.js and Go
- Developer experience: aims to improve productivity by 200%–300%
- Modern and standards‑based: rich type hints, full OpenAPI and JSON Schema support
- Automatic interactive docs out of the box
- Data validation powered by Pydantic
- First‑class async/await for high‑concurrency workloads`,
      poem: `A city of APIs, raised on speed,
Contracts in types, each path its creed.
Async couriers, stars in flight,
Every request a bolt of light.

Pydantic wardens guard the gate,
No wayward shapes can slip their fate.
Dependencies, like rivers, flow—
Uncoupled code, less toil to know.

At /docs the scroll unrolls,
Maps of routes and all their roles.
No scribe required, from code it springs—
Efficiency, with open wings.`,
      novel: `Elara, a sorcerer of data, had grown weary of lumbering “all‑in‑one” rites and fiddly, bolt‑on charms. She dreamt of a City of Swiftness where information would move as quickly as thought.

She found the keystone—an asynchronous heart—and began weaving streets with async/await. Upon each road she carved precise runes of type, and the city learned to shape itself.

Pydantic golems took their posts at every gate, politely but firmly turning away malformed travellers. In the square, a crystal of knowledge mirrored each street the moment it was built, revealing clear maps and instructions to all who visited.

Pipes laid themselves wherever they were declared, and the city thrummed with effortless order. Before long, the City of Swiftness was famed for its responsiveness and calm reliability. Its name was FastAPI—a tale of speed, rigour, and openness.`
    }
  }
  // zh‑TW default
  return {
    repo_url: 'https://github.com/tiangolo/fastapi',
    insight_report: `FastAPI 是一個現代化、為速度而生的 Python Web 框架，專注於構建 API。

核心特徵：
- 極致的效能：速度可與 Node.js 及 Go 相媲美
- 開發者體驗優先：旨在將開發效率提升 200%～300%
- 現代化與標準化：大量使用型別註記，完全遵循 OpenAPI 與 JSON Schema
- 自動生成互動式文件，開箱即用
- 以 Pydantic 進行資料驗證
- 一流的 async/await 支援，適合高併發情境`,
    poem: `一座 API 之城，由速度築成，
型別為契約，路徑其名。
異步如星，夜空急行，
每次請求，皆化作光。

Pydantic 衛兵，把守城門，
不容形狀，差之毫釐。
依賴如河，奔流注入，
解耦成詩，減卻煩憂。

/docs 展卷，路網圖成，
不經刀筆，自代言說。
效率如翼，自程式生，
在開放中，自由飛行。`,
    novel: `伊拉拉是位資料術士，厭倦了笨重的「大雜燴」法陣與東拼西湊的小咒。她夢想建造一座飛速之城，資訊能像念頭一樣迅疾。

她找到了城心——一顆異步的核心，以 async/await 編織街道；在每條路上刻下精確的型別符文，城市便能自我成形。

Pydantic 魔像駐守城門，禮貌卻堅定地拒絕畸形的旅人。廣場中央的知識水晶會在新路鋪就之際，同步映出清晰地圖與說明，來者一看便懂。

只要在藍圖上聲明，管道便自動鋪設；城市以秩序而脈動。很快，這座飛速之城憑藉響應與穩定聞名四方。它名為 FastAPI——一段關於速度、嚴謹與開放的傳奇。`
  }
})

async function handleRepoSubmit(url, presets = {}) {
  isLoading.value = true
  currentWork.value = null
  error.value = null

  try {
    const response = await generateWork(url, {
      ...presets,
      lang: lang.value,
      locale: lang.value === 'en' ? 'en-GB' : 'zh-TW'
    })
    currentWork.value = response
  } catch (err) {
    error.value = lang.value === 'en' ? 'Creation failed. Please check the URL or try again later.' : '創作失敗，請檢查 URL 是否正確或稍後再試。'
    console.error(err)
  } finally {
    isLoading.value = false
  }
}

function clearError() {
  error.value = null
}

function toggleChat() {
  isChatOpen.value = !isChatOpen.value
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

#app {
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  overflow-x: hidden; /* 防止水平滾動 */
}

.app-header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 0.75rem 0;
  text-align: center;
  color: white;
}

.header-content {
  width: 100%;
  margin: 0;
  padding: 0;
}

.app-title {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.title-icon {
  font-size: 1.8rem;
}

.app-subtitle {
  font-size: 0.95rem;
  opacity: 0.9;
}

.main-content {
  flex: 1;
  background: #f8f9fa;
  padding: 0;
}

.example-section {
  margin-bottom: 1rem;
}

.example-header {
  text-align: center;
  margin-bottom: 0.75rem;
}

.example-header h2 {
  font-size: 1.25rem;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.example-header p {
  color: #7f8c8d;
  font-size: 0.95rem;
}

.divider {
  height: 2px;
  background: linear-gradient(90deg, transparent, #667eea, transparent);
  margin: 1.25rem auto;
  max-width: 120px;
}

.loading-section {
  text-align: center;
  padding: 4rem 2rem;
}

.loading-animation {
  max-width: 400px;
  margin: 0 auto;
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border: 4px solid #e1e8ed;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 2rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-animation h3 {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.loading-animation p {
  color: #7f8c8d;
  font-size: 1rem;
}

.error-section {
  text-align: center;
  padding: 2rem;
}

.error-content {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.error-content h3 {
  color: #e74c3c;
  margin-bottom: 1rem;
}

.error-content p {
  color: #7f8c8d;
  margin-bottom: 1.5rem;
}

.retry-btn {
  padding: 0.75rem 1.5rem;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
}

.retry-btn:hover {
  background: #2980b9;
  transform: translateY(-2px);
}

.app-footer {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  text-align: center;
  padding: 1rem;
}

.app-footer a {
  color: white;
  text-decoration: none;
}

.app-footer a:hover {
  text-decoration: underline;
}

/* 聊天按鈕樣式 */
.chat-toggle-btn {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-toggle-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
}

.chat-toggle-btn.active {
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  box-shadow: 0 4px 20px rgba(231, 76, 60, 0.4);
}

.chat-toggle-btn.active:hover {
  box-shadow: 0 6px 25px rgba(231, 76, 60, 0.6);
}

@media (max-width: 768px) {
  .app-title {
    font-size: 2rem;
    flex-direction: column;
    gap: 0.5rem;
  }

  .title-icon {
    font-size: 2rem;
  }

  .app-subtitle {
    font-size: 1rem;
  }

  .header-content {
    padding: 0 1rem;
  }
}
.results-slot { margin-bottom: 1rem; }
</style>

