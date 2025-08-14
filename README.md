# Repo Saga Engine 🎭

一個將 GitHub 項目轉化為詩歌與小說的魔法引擎。通過分析代碼結構和內容，自動生成富有創意的文學作品。

## 項目概述

Repo Saga Engine 是一個全棧應用，包含：
- **後端 (FastAPI)**: 提供 API 服務，分析 GitHub 項目並生成文學作品
- **前端 (Vue 3 + Vite)**: 用戶界面，提供項目輸入和結果展示

## 項目結構

```
.
├── repo-saga-backend/          # 後端服務 (FastAPI)
│   ├── app/
│   │   ├── main.py            # FastAPI 主應用
│   │   └── services.py        # 業務邏輯服務
│   ├── requirements.txt       # Python 依賴
│   └── test_generate_api.py   # API 測試
├── repo-saga-frontend/         # 前端應用 (Vue 3)
│   ├── src/
│   │   ├── App.vue           # 主應用組件
│   │   ├── components/       # Vue 組件
│   │   └── services/         # API 服務
│   ├── package.json          # Node.js 依賴
│   └── vite.config.js        # Vite 配置
└── README.md                 # 項目說明文檔
```

## 功能特色

- 🔍 **智能分析**: 深度分析 GitHub 項目的代碼結構和內容
- 📊 **洞察報告**: 生成項目的技術洞察和分析報告
- 🎨 **詩歌創作**: 將代碼邏輯轉化為優美的詩歌
- 📚 **小說生成**: 基於項目特點創作引人入勝的小說片段
- 🌐 **現代界面**: 響應式 Vue 3 前端界面，水平三欄佈局設計
- ⚡ **高性能**: FastAPI 後端提供快速 API 響應
- 🧙‍♂️ **AI 聊天助手**: 擬人化的魔法助手，提供程式設計建議和創意靈感
- 📱 **優化體驗**: 響應式佈局設計，三欄內容獨立滾動，充分利用螢幕空間

## 快速開始

### 環境要求

- **Python**: 3.8+
- **Node.js**: 20.19.0+ 或 22.12.0+
- **npm**: 最新版本

### 1. 克隆項目

```bash
git clone <your-repo-url>
cd <project-directory>
```

### 2. 啟動後端服務

```bash
# 進入後端目錄
cd repo-saga-backend

# 安裝 Python 依賴
pip install -r requirements.txt

# 啟動 FastAPI 服務器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

後端服務將在 `http://localhost:8000` 啟動

### 3. 啟動前端服務

打開新的終端窗口：

```bash
# 進入前端目錄
cd repo-saga-frontend

# 安裝 Node.js 依賴
npm install

# 啟動開發服務器
npm run dev
```

前端應用將在 `http://localhost:5173` 啟動

### 4. 訪問應用

在瀏覽器中打開 `http://localhost:5173`，即可開始使用 Repo Saga Engine！

## API 文檔

### 主要端點

- `GET /`: API 歡迎信息
- `GET /example`: 獲取 FastAPI 示例數據
- `POST /generate`: 生成文學作品

### 使用示例

```bash
# 生成文學作品
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://github.com/tiangolo/fastapi"}'
```

### API 文檔

啟動後端服務後，可以訪問：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 開發指南

### 後端開發

```bash
cd repo-saga-backend

# 安裝依賴
pip install -r requirements.txt

# 運行測試
python test_generate_api.py

# 啟動開發服務器
uvicorn app.main:app --reload
```

### 前端開發

```bash
cd repo-saga-frontend

# 安裝依賴
npm install

# 開發模式
npm run dev

# 構建生產版本
npm run build

# 預覽生產版本
npm run preview
```

## 技術棧

### 後端
- **FastAPI**: 現代、快速的 Python Web 框架
- **Uvicorn**: ASGI 服務器
- **Requests**: HTTP 請求庫
- **Python-dotenv**: 環境變量管理

### 前端
- **Vue 3**: 漸進式 JavaScript 框架
- **Vite**: 下一代前端構建工具
- **Axios**: HTTP 客戶端
- **CSS3**: 現代樣式設計

## 部署

### 生產環境部署

1. **後端部署**:
```bash
cd repo-saga-backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

2. **前端部署**:
```bash
cd repo-saga-frontend
npm install
npm run build
# 將 dist/ 目錄部署到靜態文件服務器
```

## 貢獻指南

1. Fork 本項目
2. 創建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 許可證

本項目採用 MIT 許可證 - 查看 [LICENSE](LICENSE) 文件了解詳情。

## 聯繫方式

如有問題或建議，請通過以下方式聯繫：
- 提交 Issue
- 發送 Pull Request
- 聯繫項目維護者

---

**讓代碼變成詩歌，讓項目化為故事！** ✨
