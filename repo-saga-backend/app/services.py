import os
import re
import requests
import logging
from typing import Tuple, List, Dict

# 設置 logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = os.environ.get("OPENROUTER_MODEL", "openai/gpt-oss-20b")


def _require_openrouter_api_key() -> str:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing OPENROUTER_API_KEY environment variable. Please set it to use OpenRouter."
        )
    return api_key


def openrouter_chat(messages: List[Dict[str, str]], model: str = DEFAULT_MODEL, temperature: float = 0.7) -> str:
    """
    Call OpenRouter chat completions API and return text content.
    Requires env OPENROUTER_API_KEY. Optional envs:
      - OPENROUTER_SITE_URL (HTTP-Referer)
      - OPENROUTER_APP_TITLE (X-Title)
    """
    logger.info(f"🚀 Starting OpenRouter API call with model: {model}")
    logger.info(f"📝 Messages count: {len(messages)}")
    logger.info(f"🌡️ Temperature: {temperature}")

    api_key = _require_openrouter_api_key()
    logger.info(f"🔑 API key loaded: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else 'short'}")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    site_url = os.environ.get("OPENROUTER_SITE_URL")
    app_title = os.environ.get("OPENROUTER_APP_TITLE")
    if site_url:
        headers["HTTP-Referer"] = site_url
        logger.info(f"🌐 HTTP-Referer: {site_url}")
    if app_title:
        headers["X-Title"] = app_title
        logger.info(f"📋 X-Title: {app_title}")

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    logger.info(f"📤 Request URL: {OPENROUTER_API_BASE}/chat/completions")
    logger.info(f"📤 Request headers: {dict((k, v if k != 'Authorization' else f'Bearer {v[7:17]}...' ) for k, v in headers.items())}")
    logger.info(f"📤 Request payload keys: {list(payload.keys())}")
    logger.info(f"📤 First message preview: {messages[0] if messages else 'No messages'}")

    try:
        resp = requests.post(f"{OPENROUTER_API_BASE}/chat/completions", json=payload, headers=headers, timeout=60)
        logger.info(f"📥 Response status: {resp.status_code}")
        logger.info(f"📥 Response headers: {dict(resp.headers)}")

        resp.raise_for_status()
        data = resp.json()
        logger.info(f"📥 Response data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")

        # Expecting choices[0].message.content
        content = (
            data.get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
        )

        if not content:
            logger.error(f"❌ OpenRouter returned empty content. Full response: {data}")
            raise RuntimeError("OpenRouter returned empty content")

        logger.info(f"✅ Successfully got content, length: {len(content)} chars")
        logger.info(f"✅ Content preview: {content[:100]}...")
        return content

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Request failed: {e}")
        logger.error(f"❌ Response text (if any): {getattr(e.response, 'text', 'No response text')}")
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        raise


def extract_repo_info_from_url(url: str) -> Tuple[str, str]:
    """
    从 GitHub URL 中提取仓库信息
    """
    pattern = r'github\.com/([^/]+)/([^/]+)'
    match = re.search(pattern, url)

    if match:
        owner = match.group(1)
        repo = match.group(2)
        repo = repo.replace('.git', '')
        return owner, repo
    else:
        return "unknown", "unknown"


async def generate_saga_from_repo(repo_url: str, presets: Dict[str, str] | None = None) -> Tuple[str, str, str]:
    """
    从 GitHub 仓库 URL 生成文学作品（通过 OpenRouter）
    返回: (洞察报告, 诗歌, 小说)
    可選 presets: {poem_style, novel_genre, tone, language}
    """
    logger.info(f"🎭 Starting saga generation for repo: {repo_url}")
    presets = presets or {}
    poem_style = presets.get("poem_style")
    novel_genre = presets.get("novel_genre")
    tone = presets.get("tone")
    language = presets.get("language", "Traditional Chinese")
    is_english = language == "English"

    owner, repo = extract_repo_info_from_url(repo_url)
    logger.info(f"📂 Extracted repo info: {owner}/{repo}")
    logger.info(f"🌐 Language setting: {language}")

    if is_english:
        analysis_prompt = (
            f"Please analyze the GitHub project {owner}/{repo} and generate a project insight report.\n"
            f"Include the project's core functionality, technical features, design philosophy, etc., "
            f"and make reasonable inferences based on README and common directory structures."
        )
    else:
        analysis_prompt = (
            f"请分析 GitHub 项目 {owner}/{repo}，生成一份项目洞察报告。\n"
            f"需要包含项目的核心功能、技术特点、设计理念等，并尽量参考 README 与常见目录结构进行合理推断。"
        )

    try:
        logger.info("📊 Step 1/3: Generating insight report...")
        system_content = (
            "You are a senior open-source code reviewer and technical writer."
            if is_english else
            "你是一位资深的开源代码审阅者与技术作家。"
        )
        insight_report = openrouter_chat([
            {"role": "system", "content": system_content},
            {"role": "user", "content": analysis_prompt},
        ])
        logger.info(f"✅ Step 1/3 completed. Insight report length: {len(insight_report)} chars")

        logger.info("🎨 Step 2/3: Generating poem...")
        if is_english:
            style_hint = f"Style: {poem_style}. " if poem_style else ""
            tone_hint = f"Tone: {tone}. " if tone else ""
            poem_prompt = (
                f"Based on the following project insight report, create a poem about the {owner}/{repo} project:\n"
                f"{insight_report}\n\n"
                f"{style_hint}{tone_hint}"
                f"Requirements: Be imaginative, reflect the beauty of code and the spirit of the project, "
                f"with clear stanzas for easy interface display."
            )
            system_content = "You are a modern poet who specializes in technical themes."
        else:
            style_hint = f"風格：{poem_style}。" if poem_style else ""
            tone_hint = f"語氣：{tone}。" if tone else ""
            poem_prompt = (
                f"基于以下项目洞察报告，创作一首关于 {owner}/{repo} 项目的诗歌：\n"
                f"{insight_report}\n\n"
                f"{style_hint}{tone_hint}"
                f"要求：富有想象力，体现代码的美感和项目的精神，分段清晰，便于界面展示。"
            )
            system_content = "你是一位擅长技术题材的现代诗歌创作者。"

        poem = openrouter_chat([
            {"role": "system", "content": system_content},
            {"role": "user", "content": poem_prompt},
        ], temperature=0.9)
        logger.info(f"✅ Step 2/3 completed. Poem length: {len(poem)} chars")

        logger.info("📚 Step 3/3: Generating novel...")
        if is_english:
            genre_hint = f"Novel genre: {novel_genre}. " if novel_genre else ""
            tone_hint2 = f"Tone: {tone}. " if tone else ""
            novel_prompt = (
                f"Based on the following project insight report, create a short story about the {owner}/{repo} project:\n"
                f"{insight_report}\n\n"
                f"{genre_hint}{tone_hint2}"
                f"Requirements: Include plot and characters, reflect the story behind the project "
                f"and the spirit of the developers, with appropriate length."
            )
            system_content = "You are a novelist who can blend technology with humanities."
        else:
            genre_hint = f"小說類型：{novel_genre}。" if novel_genre else ""
            tone_hint2 = f"語氣：{tone}。" if tone else ""
            novel_prompt = (
                f"基于以下项目洞察报告，创作一篇关于 {owner}/{repo} 项目的短篇小说：\n"
                f"{insight_report}\n\n"
                f"{genre_hint}{tone_hint2}"
                f"要求：有情节，有人物，体现项目背后的故事和开发者的精神，篇幅适中。"
            )
            system_content = "你是一位能够将技术与人文融合的小说作者。"

        novel = openrouter_chat([
            {"role": "system", "content": system_content},
            {"role": "user", "content": novel_prompt},
        ])
        logger.info(f"✅ Step 3/3 completed. Novel length: {len(novel)} chars")

        logger.info("🎉 All steps completed successfully!")
        return insight_report.strip(), poem.strip(), novel.strip()

    except Exception as e:
        logger.error(f"❌ Error in generate_saga_from_repo: {e}")
        logger.error(f"❌ Error type: {type(e).__name__}")
        # 交由上層捕獲並返回友好提示
        raise


# FastAPI 示例数据
FASTAPI_EXAMPLE = {
    "repo_url": "https://github.com/tiangolo/fastapi",
    "insight_report": """FastAPI 是一个现代化、为速度而生的 Python Web 框架，专注于构建 API。

核心特征：
- 极致的性能：速度可以和 NodeJS 及 Go 语言相媲美
- 开发者体验优先：旨在将开发效率提升200%-300%
- 现代化与标准化：大量使用类型提示，完全遵循 OpenAPI 和 JSON Schema
- 自动文档生成：无需额外工作就能生成交互式 API 文档
- 数据验证：基于 Pydantic 的自动数据验证
- 异步处理：基于 async/await，适合高并发场景""",

    "poem": """一座API之城，由速度筑成，
类型为契约，路径是其名。
异步的协程，如星辰夜奔，
每一次请求，都迅捷如风。

Pydantic卫兵，严守着城门，
验证所有过客，不差分毫。
依赖被注入，似活水流深，
解耦了代码，免去了纷扰。

Swagger卷轴，在 /docs 展开，
描绘着路径，城市的地图。
无需一笔一划，它自己到来，
从代码深处，升起高效的国度。""",

    "novel": """伊拉拉是一位数据术士，她厌倦了古老而缓慢的"全家桶"式咒语和需要自己动手搭建一切的"散件"式魔法。她梦想建造一座"飞速之城"，在那里，信息的流动应该像思想一样快。

她找到了城市的基石——名为"星之石"的异步核心，并开始用 async/await 的魔力编织城市的街道。她没有使用传统的砖块，而是为每一条街道、每一座建筑都刻上了精确的"类型符文"。

奇迹发生了。这些符文不仅定义了建筑的结构，还自动吸引来了城市的卫兵——Pydantic 魔像。这些魔像不知疲倦地守在每一个入口，任何形态错误的数据都会被它们礼貌而坚定地拒绝。

更神奇的是，每当伊拉拉完成一条街道的建设，城市中央的"知识水晶"就会自动浮现出这条街道的精确地图和使用方法，任何来访者都能一目了然地知道如何与这座城市互动。

城里的"管道系统"也与众不同。需要水源或能量的建筑，只需在蓝图上声明，城市就会自动将管道铺设过去，无需伊拉拉亲手连接。

很快，伊拉拉的"飞速之城"以其惊人的响应速度、坚不可摧的稳定性和对开发者极度友好的特性而闻名于世。它的名字就叫 FastAPI，一个关于速度、严谨与开放的传奇。"""
}
