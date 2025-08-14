<template>
  <div class="lang-switcher">
    <select v-model="langModel" @change="onChange">
      <option value="en">English</option>
      <option value="zh-TW">繁體中文</option>
    </select>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from '../i18n'

const { lang, setLang } = useI18n()
const langModel = computed({
  get: () => lang.value,
  set: (v) => setLang(v)
})
const onChange = () => {}
</script>

<style scoped>
.lang-switcher {
  position: fixed;
  top: 10px;
  right: 10px;
  z-index: 1100;
}
select { padding: 6px 8px; border-radius: 6px; border: 1px solid #ddd; }
</style>

