<template>
  <div class="repo-input-container">
    <div class="input-section">
      <h2>{{ t('input.title') }}</h2>
      <p class="subtitle">{{ t('input.subtitle') }}</p>

      <!-- 風格選擇器 -->
      <div class="style-presets">
        <select v-model="poemStyle" class="preset-select">
          <option value="">{{ t('input.presets.poemStyleDefault') }}</option>
          <option value="tang">{{ t('input.presets.poemStyle.tang') }}</option>
          <option value="haiku">{{ t('input.presets.poemStyle.haiku') }}</option>
          <option value="modern">{{ t('input.presets.poemStyle.modern') }}</option>
        </select>
        <select v-model="novelGenre" class="preset-select">
          <option value="">{{ t('input.presets.novelGenreDefault') }}</option>
          <option value="mystery">{{ t('input.presets.novelGenre.mystery') }}</option>
          <option value="romance">{{ t('input.presets.novelGenre.romance') }}</option>
          <option value="fantasy">{{ t('input.presets.novelGenre.fantasy') }}</option>
          <option value="scifi">{{ t('input.presets.novelGenre.scifi') }}</option>
        </select>
        <select v-model="tone" class="preset-select">
          <option value="">{{ t('input.presets.toneDefault') }}</option>
          <option value="serious">{{ t('input.presets.tone.serious') }}</option>
          <option value="humour">{{ t('input.presets.tone.humour') }}</option>
          <option value="lyrical">{{ t('input.presets.tone.lyrical') }}</option>
        </select>
      </div>

      <form @submit.prevent="handleSubmit" class="input-form">
        <div class="input-group">
          <input
            v-model="repoUrl"
            type="url"
            :placeholder="t('input.placeholder')"
            class="repo-input"
            :disabled="isLoading"
            required
          />
          <button 
            type="submit" 
            class="generate-btn"
            :disabled="isLoading || !repoUrl.trim()"
          >
            <span v-if="!isLoading">✨ {{ t('input.generate') }}</span>
            <span v-else>🎭 {{ t('input.generating') }}</span>
          </button>
        </div>
      </form>
      
      <div class="examples">
        <p>{{ t('input.examplesTitle') }}</p>
        <div class="example-links">
          <button 
            @click="setExample('https://github.com/microsoft/vscode')"
            class="example-btn"
          >
            VS Code
          </button>
          <button 
            @click="setExample('https://github.com/facebook/react')"
            class="example-btn"
          >
            React
          </button>
          <button 
            @click="setExample('https://github.com/vuejs/vue')"
            class="example-btn"
          >
            Vue.js
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from '../i18n'

const props = defineProps({
  isLoading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit'])

const { t } = useI18n()
const repoUrl = ref('')
const poemStyle = ref('')
const novelGenre = ref('')
const tone = ref('')

const handleSubmit = () => {
  if (repoUrl.value.trim()) {
    emit('submit', repoUrl.value.trim(), {
      poem_style: poemStyle.value || undefined,
      novel_genre: novelGenre.value || undefined,
      tone: tone.value || undefined,
    })
  }
}

const setExample = (url) => {
  repoUrl.value = url
}
</script>

<style scoped>
.repo-input-container {
  width: 100%;
  margin: 0;
  padding: 0;
}

.input-section {
  text-align: center;
}

.input-section h2 {
  font-size: 1.25rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 0.4rem;
}

.subtitle {
  font-size: 0.95rem;
  color: #7f8c8d;
  margin-bottom: 1rem;
}

.input-form {
  margin-bottom: 2rem;
}

.input-group {
  display: flex;
  gap: 0.5rem; /* 減少間距 */
  width: 100%;
  margin: 0;
}

.repo-input {
  flex: 1;
  padding: 1rem;
  font-size: 1rem;
  border: 2px solid #e1e8ed;
  border-radius: 8px;
  transition: border-color 0.3s ease;
}

.repo-input:focus {
  outline: none;
  border-color: #3498db;
}

.repo-input:disabled {
  background-color: #f8f9fa;
  cursor: not-allowed;
}

.generate-btn {
  padding: 0.5rem 1rem;
  font-size: 0.95rem;
  font-weight: bold;
  color: white;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.generate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.examples {
  margin-top: 2rem;
}

.examples p {
  color: #7f8c8d;
  margin-bottom: 1rem;
}

.example-links {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.example-btn {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  color: #3498db;
  background: transparent;
  border: 1px solid #3498db;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.example-btn:hover {
  background: #3498db;
  color: white;
}

@media (max-width: 768px) {
  .input-group { flex-direction: column; }
  .input-section h2 { font-size: 1.1rem; }
}
.style-presets { display: flex; gap: 0.5rem; justify-content: center; margin: 0.5rem 0 1rem; }
.preset-select { padding: 0.4rem 0.6rem; border: 1px solid #ddd; border-radius: 6px; background: #fff; }

@media (max-width: 768px) {
  .style-presets { flex-direction: column; align-items: center; }
  .preset-select { width: 95%; }
}
</style>

