import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from .services import generate_saga_from_repo, openrouter_chat, FASTAPI_EXAMPLE

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="Repo Saga Engine",
    description="An API that turns GitHub repositories into literature.",
)

# 配置 CORS，允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应指定前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RepoURLRequest(BaseModel):
    url: str
    poem_style: Optional[str] = None  # e.g., 唐詩、俳句、現代詩
    novel_genre: Optional[str] = None  # e.g., 懸疑、愛情、奇幻、科幻
    tone: Optional[str] = None  # e.g., 嚴肅、幽默、抒情
    lang: Optional[str] = None  # e.g., 'en', 'zh-TW'
    locale: Optional[str] = None  # e.g., 'en-GB', 'zh-TW'

class ChatRequest(BaseModel):
    message: str
    conversation_history: list = []
    lang: Optional[str] = None  # e.g., 'en', 'zh-TW'
    locale: Optional[str] = None  # e.g., 'en-GB', 'zh-TW'

class ChatResponse(BaseModel):
    response: str

class LiteraryWorkResponse(BaseModel):
    repo_url: str
    insight_report: str
    poem: str
    novel: str

@app.get("/")
async def root():
    """
    根路径，返回 API 信息
    """
    return {"message": "Welcome to Repo Saga Engine API"}

@app.get("/example")
async def get_example():
    """
    返回 FastAPI 的示例数据
    """
    return FASTAPI_EXAMPLE

@app.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(request: ChatRequest):
    """
    與魔法助手聊天，使用 OpenRouter AI 生成回應
    """
    try:
        # 根據語言設定決定系統提示
        is_english = request.lang == 'en' or (request.locale and request.locale.startswith('en'))

        if is_english:
            system_content = """You are the Repo Saga Assistant, a specialized AI helper for the Repo Saga Engine platform. Your primary purpose is to help users understand and optimize their experience with transforming GitHub repositories into poetry and fiction.

Your expertise includes:

1. Repository Analysis: Explaining how the platform analyzes GitHub projects, what information is extracted, and how it's processed
2. Literary Transformation: Guiding users on how to get better poetry and novel outputs, explaining different styles and tones available
3. Platform Features: Helping users understand the interface, settings, and customization options
4. Creative Optimization: Providing tips for selecting repositories that work well for literary transformation
5. Technical Support: Assisting with any issues related to URL input, generation process, or output quality

You should focus specifically on Repo Saga Engine functionality and avoid general programming discussions unless they directly relate to improving the literary transformation process.

Always respond in English with a helpful and knowledgeable tone."""
        else:
            system_content = """你是 Repo Saga 助手，專門為 Repo Saga Engine 平台提供協助的 AI 助理。你的主要目的是幫助用戶理解並優化他們將 GitHub 倉庫轉化為詩歌和小說的體驗。

你的專業領域包括：

1. 倉庫分析：解釋平台如何分析 GitHub 專案、提取哪些資訊，以及如何處理這些資訊
2. 文學轉化：指導用戶如何獲得更好的詩歌和小說輸出，解釋可用的不同風格和語調
3. 平台功能：幫助用戶理解介面、設定和自訂選項
4. 創意優化：提供選擇適合文學轉化的倉庫的技巧
5. 技術支援：協助解決與 URL 輸入、生成過程或輸出品質相關的任何問題

你應該專注於 Repo Saga Engine 的功能，避免一般性的程式設計討論，除非它們直接關係到改善文學轉化過程。

請用繁體中文回應，語氣要有幫助且專業。"""

        # 構建對話歷史
        messages = [
            {
                "role": "system",
                "content": system_content
            }
        ]

        # 添加對話歷史（最多保留最近 10 輪對話）
        if request.conversation_history:
            recent_history = request.conversation_history[-20:]  # 最多 20 條消息（10 輪對話）
            messages.extend(recent_history)

        # 添加當前用戶消息
        messages.append({"role": "user", "content": request.message})

        # 調用 OpenRouter API
        response = openrouter_chat(
            messages=messages,
            model="openai/gpt-oss-20b",
            temperature=0.8  # 稍高的溫度讓回應更有創意
        )

        return ChatResponse(response=response)

    except Exception as e:
        # 如果 AI 調用失敗，返回一個友好的錯誤回應
        is_english = request.lang == 'en' or (request.locale and request.locale.startswith('en'))

        if is_english:
            fallback_responses = [
                "Sorry, the Repo Saga Assistant service is temporarily unavailable. Please try again later. In the meantime, feel free to explore the platform's features!",
                "I'm experiencing some technical difficulties right now. Please try again in a moment. You can continue using the main repository transformation features.",
                "The assistant service is currently offline. Please try again later. The core Repo Saga Engine functionality remains available for your use."
            ]
        else:
            fallback_responses = [
                "抱歉，Repo Saga 助手服務暫時無法使用，請稍後再試。在等待期間，歡迎繼續探索平台的其他功能！",
                "我目前遇到一些技術問題，請稍後再試。你可以繼續使用主要的倉庫轉化功能。",
                "助手服務目前離線中，請稍後再試。Repo Saga Engine 的核心功能仍然可以正常使用。"
            ]

        import random
        return ChatResponse(response=random.choice(fallback_responses))

@app.post("/generate", response_model=LiteraryWorkResponse)
async def generate_literary_work(request: RepoURLRequest):
    """
    Accepts a GitHub repo URL and returns its literary transformation.
    """
    try:
        # 確定語言設定
        is_english = request.lang == 'en' or (request.locale and request.locale.startswith('en'))

        presets = {
            "poem_style": request.poem_style,
            "novel_genre": request.novel_genre,
            "tone": request.tone,
            "language": "English" if is_english else "Traditional Chinese",
        }
        insight_report, poem, novel = await generate_saga_from_repo(request.url, presets)

        return LiteraryWorkResponse(
            repo_url=request.url,
            insight_report=insight_report,
            poem=poem,
            novel=novel
        )
    except Exception as e:
        # 根據語言返回對應的錯誤信息
        is_english = request.lang == 'en' or (request.locale and request.locale.startswith('en'))

        if is_english:
            error_insight = f"Sorry, unable to analyze project {request.url}. Please check if the URL is correct."
            error_poem = "The world of code is full of mystery,\nSometimes we lose our way.\nBut this is the joy of exploration,\nEvery attempt is growth."
            error_novel = "In a corner of the digital world, a mysterious project awaits discovery. Though this exploration encountered difficulties, brave developers never give up their quest for truth."
        else:
            error_insight = f"抱歉，无法分析项目 {request.url}。请检查 URL 是否正确。"
            error_poem = "代码的世界充满未知，\n有时我们会迷失方向。\n但这正是探索的乐趣，\n每一次尝试都是成长。"
            error_novel = "在数字世界的某个角落，一个神秘的项目等待着被发现。虽然这次的探索遇到了困难，但勇敢的开发者们永远不会放弃寻找真理的脚步。"

        return LiteraryWorkResponse(
            repo_url=request.url,
            insight_report=error_insight,
            poem=error_poem,
            novel=error_novel
        )


