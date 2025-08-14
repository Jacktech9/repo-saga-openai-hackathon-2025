<template>
  <div class="results-container">
    <div class="results-header" v-if="!hideHeader">
      <h2>✨ {{ t('results.done') }}</h2>
      <p class="repo-info">
        <span class="repo-label">{{ t('results.project') }}：</span>
        <a :href="work.repo_url" target="_blank" class="repo-link">
          {{ getRepoName(work.repo_url) }}
        </a>
      </p>
    </div>

    <div v-if="!headerOnly" class="content-grid">
      <!-- 專案洞察報告 -->
      <div class="content-section insight-section">
        <div class="section-header">
          <h3>🔍 {{ t('sections.insight') }}</h3>
        </div>
        <div class="content-body">
          <pre class="insight-text">{{ work.insight_report }}</pre>
        </div>
      </div>

      <!-- 詩歌 -->
      <div class="content-section poem-section">
        <div class="section-header">
          <h3>📝 {{ t('sections.poem') }}</h3>
        </div>
        <div class="content-body">
          <div class="poem-text">{{ work.poem }}</div>
        </div>
      </div>

      <!-- 小說 -->
      <div class="content-section novel-section">
        <div class="section-header">
          <h3>📚 {{ t('sections.novel') }}</h3>
        </div>
        <div class="content-body">
          <div class="novel-text">{{ work.novel }}</div>
        </div>
      </div>
    </div>

    <div v-if="!headerOnly" class="actions">
      <button @click="copyToClipboard" class="action-btn copy-btn">
        📋 {{ t('results.copy') }}
      </button>
      <button @click="downloadAsText" class="action-btn download-btn">
        💾 {{ t('results.download') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from '../i18n'

const props = defineProps({
  work: {
    type: Object,
    required: true
  },
  hideHeader: {
    type: Boolean,
    default: false
  },
  headerOnly: {
    type: Boolean,
    default: false
  }
})

const getRepoName = (url) => {
  try {
    const match = url.match(/github\.com\/([^\/]+\/[^\/]+)/)
    return match ? match[1] : url
  } catch {
    return url
  }
}

const { t, lang } = useI18n()

const copyToClipboard = async () => {
  const colon = lang.value === 'en' ? ':' : '：'
  const content = `
${t('results.project')}${colon} ${props.work.repo_url}

${t('sections.insight')}${colon}
${props.work.insight_report}

${t('sections.poem')}${colon}
${props.work.poem}

${t('sections.novel')}${colon}
${props.work.novel}
  `.trim()

  try {
    await navigator.clipboard.writeText(content)
    alert(lang.value === 'en' ? 'Copied to clipboard.' : '已複製到剪貼簿！')
  } catch (err) {
    console.error('Copy failed:', err)
    alert(lang.value === 'en' ? 'Copy failed. Please copy manually.' : '複製失敗，請手動選取文字複製')
  }
}

const downloadAsText = () => {
  const colon = lang.value === 'en' ? ':' : '：'
  const content = `
${t('results.project')}${colon} ${props.work.repo_url}

${t('sections.insight')}${colon}
${props.work.insight_report}

${t('sections.poem')}${colon}
${props.work.poem}

${t('sections.novel')}${colon}
${props.work.novel}
  `.trim()

  const blob = new Blob([content], { type: 'text/plain;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `repo-saga-${getRepoName(props.work.repo_url).replace('/', '-')}.txt`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
.results-container {
  width: 100%;
  margin: 0;
  padding: 0;
}

.results-header {
  text-align: center;
  margin-bottom: 0.5rem;
}

.results-header h2 {
  font-size: 1.25rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.repo-info {
  font-size: 0.95rem;
  color: #7f8c8d;
}

.repo-label {
  font-weight: bold;
}

.repo-link {
  color: #3498db;
  text-decoration: none;
  font-weight: bold;
}

.repo-link:hover {
  text-decoration: underline;
}

.content-grid {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap; /* 防止換行導致疊到下方 */
  gap: 0.3rem;
  margin-bottom: 0.5rem;
  height: 45vh; /* 縮小結果區塊高度，避免佔滿視窗 */
  min-height: 320px;
}

.content-section {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease;
  flex: 1; /* 每個區域平均分配寬度 */
  display: flex;
  flex-direction: column;
  height: 100%; /* 使用父容器的完整高度 */
}

.content-section:hover {
  transform: translateY(-2px);
}

.section-header {
  padding: 0.4rem 0.6rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  flex-shrink: 0;
}

.section-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: bold;
}

.content-body {
  padding: 0.5rem; /* 進一步減少內邊距 */
  overflow-y: auto;
  flex: 1; /* 內容區域佔用剩餘空間 */
  height: 0; /* 配合 flex: 1 使用，確保正確的高度計算 */
}

/* 自定義滾動條樣式 */
.content-body::-webkit-scrollbar {
  width: 8px;
}

.content-body::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.content-body::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px;
}

.content-body::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
}

.insight-text {
  font-family: 'Courier New', monospace;
  font-size: 0.95rem;
  line-height: 1.55;
  color: #2c3e50;
  white-space: pre-wrap;
  margin: 0;
}

.poem-text {
  font-family: 'Georgia', serif;
  font-size: 1rem;
  line-height: 1.6;
  color: #2c3e50;
  white-space: pre-line;
  text-align: center;
  font-style: italic;
}

.novel-text {
  font-family: 'Georgia', serif;
  font-size: 0.95rem;
  line-height: 1.6;
  color: #2c3e50;
  white-space: pre-line;
  text-align: justify;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.action-btn {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.copy-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.download-btn {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* 移除響應式網格佈局，改為垂直排列 */

@media (max-width: 600px) {
  .content-grid {
    flex-direction: column;
    height: auto;
  }

  .content-section {
    height: 240px; /* 手機/平板時再縮小 */
  }
}

@media (max-width: 768px) {
  .results-container { padding: 0.5rem; }
  .results-header h2 { font-size: 1.1rem; }
}
</style>

