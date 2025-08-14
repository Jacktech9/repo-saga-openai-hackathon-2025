import { ref } from 'vue'

// Simple in-app i18n without extra deps
const lang = ref(localStorage.getItem('lang') || 'en')

const messages = {
  en: {
    app: {
      title: 'Repo Saga Engine',
      subtitle: 'Turn GitHub projects into poetry and fiction',
    },
    example: {
      title: 'Case Study: FastAPI',
      desc: 'See how we transform the famous FastAPI framework into literature',
    },
    input: {
      title: 'Enter GitHub repository URL',
      subtitle: 'Let us transform your code into poetry and stories',
      placeholder: 'https://github.com/username/repository',
      generate: 'Generate Literature',
      generating: 'Creating...',
      examplesTitle: 'Try these popular projects:',
      presets: {
        poemStyleDefault: 'Poetry style (default)',
        poemStyle: { tang: 'Tang poetry', haiku: 'Haiku', modern: 'Modern verse' },
        novelGenreDefault: 'Novel genre (default)',
        novelGenre: { mystery: 'Mystery', romance: 'Romance', fantasy: 'Fantasy', scifi: 'Science fiction' },
        toneDefault: 'Tone (default)',
        tone: { serious: 'Serious', humour: 'Humour', lyrical: 'Lyrical' }
      }
    },
    results: {
      done: 'Literary Work Ready',
      project: 'Project',
      copy: 'Copy All',
      download: 'Download as Text',
    },
    sections: {
      insight: 'Project Insight Report',
      poem: 'Code Poem',
      novel: 'Code Novel',
    },
  },
  'zh-TW': {
    app: {
      title: 'Repo Saga Engine',
      subtitle: '將 GitHub 專案轉化為詩歌與小說的魔法引擎',
    },
    example: {
      title: '案例展示：FastAPI',
      desc: '看看我們如何將著名的 FastAPI 框架轉化為文學作品',
    },
    input: {
      title: '輸入 GitHub 倉庫 URL',
      subtitle: '讓我們把你的程式碼化作詩與故事',
      placeholder: 'https://github.com/username/repository',
      generate: '生成文學作品',
      generating: '創作中...',
      examplesTitle: '試試這些熱門專案：',
      presets: {
        poemStyleDefault: '詩風（預設）',
        poemStyle: { tang: '唐詩', haiku: '俳句', modern: '現代詩' },
        novelGenreDefault: '小說類型（預設）',
        novelGenre: { mystery: '懸疑', romance: '愛情', fantasy: '奇幻', scifi: '科幻' },
        toneDefault: '語氣（預設）',
        tone: { serious: '嚴肅', humour: '幽默', lyrical: '抒情' }
      }
    },
    results: {
      done: '文學作品生成完成',
      project: '專案',
      copy: '複製全部內容',
      download: '下載為文字檔',
    },
    sections: {
      insight: '專案洞察報告',
      poem: '程式詩歌',
      novel: '程式小說',
    },
  },
}

export function useI18n() {
  const setLang = (val) => {
    lang.value = val
    localStorage.setItem('lang', val)
  }
  const t = (key) => {
    const parts = key.split('.')
    let cur = messages[lang.value] || {}
    for (const p of parts) cur = cur?.[p]
    return cur ?? key
  }
  return { lang, setLang, t }
}

