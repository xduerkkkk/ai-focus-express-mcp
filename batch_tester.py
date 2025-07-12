from web_utils import get_page_content_and_date

from datetime import datetime, timezone, timedelta
import time

# ==============================================================================
# 这是你提供的测试函数，我们把它放在这里，方便统一执行
# ==============================================================================
def test_source_compatibility(url, category):
    """测试单个信息源是否兼容我们的解析函数"""
    print(f"\n--- [{category}] 正在测试: {url} ---")
    
    # 设定一个较宽松的时间范围以增加找到文章的几率
    time_limit = datetime.now(timezone.utc) - timedelta(days=90) 
    
    try:
        # 核心调用：使用你的解析函数
        # 我们需要找到一篇实际的文章来测试，而不是博客首页。
        # 一个小技巧：使用Google搜索来自动寻找该网站上的一篇文章URL
        from googlesearch import search
        # 查找该网站上任意一篇关于 "AI" 的文章来测试
        query = f'"AI" site:{url}'
        # 我们只需要一个URL来测试即可
        test_url = next(search(query, num_results=1, lang="en"), None)

        if not test_url:
            print(f"🟡 {url} - 警告: 无法通过搜索自动找到测试文章，跳过。")
            return

        print(f"   (使用文章链接进行测试: {test_url[:70]}...)")
        result = get_page_content_and_date(test_url, time_limit)
        
        if result:
            title, date, summary = result
            print(f"✅ {url} - 成功解析")
            print(f"   标题: {title[:50]}...")
            print(f"   日期: {date.strftime('%Y-%m-%d')}")
            print(f"   摘要: {summary.strip()[:100]}...")
        else:
            print(f"❌ {url} - 解析失败 (函数返回None，可能日期过旧或无法提取内容)")

    except Exception as e:
        print(f"💥 {url} - 出现严重错误: {e}")

# ==============================================================================
# AI 信息源仓库 (URL REGISTRY)
# ==============================================================================
SOURCES_TO_TEST = {
    "顶级公司博客 (Top-Tier Company Blogs)": [
        "openai.com/blog",
        "huggingface.co/blog",
        "ai.googleblog.com",
        "developer.nvidia.com/blog",
        "ai.meta.com/blog/",
        "blogs.microsoft.com/ai/",
        "deepmind.google/blog/",
        "anthropic.com/news",
        "mistral.ai/news/"
    ],
    "AI专业新闻与社区 (AI-focused News & Community)": [
        "marktechpost.com",
        "unite.ai",
        "analyticsvidhya.com/blog",
        "kdnuggets.com",
        "towardsdatascience.com" # (在Medium上，可能会有解析困难)
    ],
    "主流科技媒体 (Major Tech Outlets)": [
        "techcrunch.com/category/artificial-intelligence/",
        "venturebeat.com/category/ai/",
        "arstechnica.com/information-technology/artificial-intelligence/",
        "wired.com/tag/artificial-intelligence/"
    ],
    "云与硬件厂商 (Cloud & Hardware Vendors)": [
        "aws.amazon.com/blogs/machine-learning/",
        "apple.com/machine-learning/research/",
        "blogs.oracle.com/ai/"
    ]
}

# ==============================================================================
# 主执行函数 (MAIN EXECUTOR)
# ==============================================================================
def main():
    print("="*50)
    print("  AI 信息源兼容性自动化测试脚本")
    print("="*50)
    
    for category, urls in SOURCES_TO_TEST.items():
        for url in urls:
            test_source_compatibility(url, category)
            time.sleep(2) # 增加延时，尊重对方服务器，避免被封禁

    print("\n\n" + "="*50)
    print("  所有测试已完成！")
    print("  请检查上面的 '✅ 成功解析' 列表，")
    print("  并将这些网址更新到你的 sources.json 文件中。")
    print("="*50)

if __name__ == "__main__":
    main()