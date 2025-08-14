#!/usr/bin/env python3
"""
測試 /generate API 的效果評估程式
測試不同類型的 GitHub 專案，評估回應品質、速度和錯誤處理
"""

import requests
import time
import json
from typing import Dict, List, Tuple
from dataclasses import dataclass

API_BASE = "http://localhost:8000"

@dataclass
class TestResult:
    repo_url: str
    success: bool
    response_time: float
    insight_length: int
    poem_length: int
    novel_length: int
    error_message: str = ""
    
    def __str__(self):
        status = "✅ SUCCESS" if self.success else "❌ FAILED"
        if self.success:
            return (f"{status} | {self.repo_url}\n"
                   f"  ⏱️  Time: {self.response_time:.1f}s\n"
                   f"  📊 Insight: {self.insight_length} chars\n"
                   f"  🎨 Poem: {self.poem_length} chars\n"
                   f"  📚 Novel: {self.novel_length} chars")
        else:
            return (f"{status} | {self.repo_url}\n"
                   f"  ❌ Error: {self.error_message}")

def test_generate_api(repo_url: str, timeout: int = 120) -> TestResult:
    """測試單一 repo 的 /generate API"""
    print(f"🧪 Testing: {repo_url}")
    
    start_time = time.time()
    try:
        response = requests.post(
            f"{API_BASE}/generate",
            json={"url": repo_url},
            timeout=timeout
        )
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            return TestResult(
                repo_url=repo_url,
                success=True,
                response_time=response_time,
                insight_length=len(data.get("insight_report", "")),
                poem_length=len(data.get("poem", "")),
                novel_length=len(data.get("novel", ""))
            )
        else:
            return TestResult(
                repo_url=repo_url,
                success=False,
                response_time=response_time,
                insight_length=0,
                poem_length=0,
                novel_length=0,
                error_message=f"HTTP {response.status_code}: {response.text[:200]}"
            )
            
    except requests.exceptions.Timeout:
        return TestResult(
            repo_url=repo_url,
            success=False,
            response_time=timeout,
            insight_length=0,
            poem_length=0,
            novel_length=0,
            error_message="Request timeout"
        )
    except Exception as e:
        return TestResult(
            repo_url=repo_url,
            success=False,
            response_time=time.time() - start_time,
            insight_length=0,
            poem_length=0,
            novel_length=0,
            error_message=str(e)
        )

def evaluate_content_quality(result: TestResult) -> Dict[str, str]:
    """評估內容品質"""
    if not result.success:
        return {"overall": "FAILED"}
    
    # 長度評估
    insight_quality = "GOOD" if result.insight_length > 500 else "SHORT" if result.insight_length > 100 else "TOO_SHORT"
    poem_quality = "GOOD" if result.poem_length > 200 else "SHORT" if result.poem_length > 50 else "TOO_SHORT"
    novel_quality = "GOOD" if result.novel_length > 800 else "SHORT" if result.novel_length > 200 else "TOO_SHORT"
    
    # 整體評估
    qualities = [insight_quality, poem_quality, novel_quality]
    if all(q == "GOOD" for q in qualities):
        overall = "EXCELLENT"
    elif any(q == "GOOD" for q in qualities) and "TOO_SHORT" not in qualities:
        overall = "GOOD"
    elif "TOO_SHORT" in qualities:
        overall = "POOR"
    else:
        overall = "FAIR"
    
    return {
        "overall": overall,
        "insight": insight_quality,
        "poem": poem_quality,
        "novel": novel_quality
    }

def main():
    """主測試函式"""
    print("🚀 Starting API Test Suite for /generate endpoint")
    print("=" * 60)
    
    # 測試用的 GitHub 專案（不同類型和規模）
    test_repos = [
        # 小型專案
        "https://github.com/octocat/Hello-World",
        
        # 中型專案
        "https://github.com/expressjs/express",
        
        # 大型專案
        "https://github.com/microsoft/vscode",
        
        # Python 專案
        "https://github.com/psf/requests",
        
        # 前端專案
        "https://github.com/vuejs/vue",
        
        # 無效 URL 測試
        "https://github.com/nonexistent/repo-that-does-not-exist"
    ]
    
    results: List[TestResult] = []
    
    # 執行測試
    for repo_url in test_repos:
        result = test_generate_api(repo_url)
        results.append(result)
        print(result)
        print("-" * 40)
        time.sleep(2)  # 避免 API 限制
    
    # 統計分析
    print("\n📊 TEST SUMMARY")
    print("=" * 60)
    
    successful_tests = [r for r in results if r.success]
    failed_tests = [r for r in results if not r.success]
    
    print(f"✅ Successful: {len(successful_tests)}/{len(results)}")
    print(f"❌ Failed: {len(failed_tests)}/{len(results)}")
    
    if successful_tests:
        avg_time = sum(r.response_time for r in successful_tests) / len(successful_tests)
        avg_insight = sum(r.insight_length for r in successful_tests) / len(successful_tests)
        avg_poem = sum(r.poem_length for r in successful_tests) / len(successful_tests)
        avg_novel = sum(r.novel_length for r in successful_tests) / len(successful_tests)
        
        print(f"\n⏱️  Average Response Time: {avg_time:.1f}s")
        print(f"📊 Average Content Lengths:")
        print(f"   Insight: {avg_insight:.0f} chars")
        print(f"   Poem: {avg_poem:.0f} chars")
        print(f"   Novel: {avg_novel:.0f} chars")
        
        # 品質評估
        print(f"\n🎯 QUALITY ASSESSMENT:")
        for result in successful_tests:
            quality = evaluate_content_quality(result)
            repo_name = result.repo_url.split('/')[-2:]
            print(f"   {'/'.join(repo_name)}: {quality['overall']} "
                  f"(I:{quality['insight']}, P:{quality['poem']}, N:{quality['novel']})")
    
    if failed_tests:
        print(f"\n❌ FAILED TESTS:")
        for result in failed_tests:
            repo_name = result.repo_url.split('/')[-2:]
            print(f"   {'/'.join(repo_name)}: {result.error_message}")
    
    print("\n🏁 Test completed!")

if __name__ == "__main__":
    main()
