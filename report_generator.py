# report_generator.py
from web_utils import search_arxiv_papers, search_website_articles

def generate_arxiv_section(papers):
    """生成ArXiv论文部分"""
    if not papers:
        return "## 🔬 ArXiv 论文成果\n\n未找到在指定时间范围内的相关论文。\n\n"
    
    results_md = "## 🔬 ArXiv 论文成果\n\n"
    for paper in papers:
        results_md += f"- **[{paper['title']}]({paper['url']})**\n"
        results_md += f"  - **作者**: {paper['authors']}\n"
        results_md += f"  - **发布日期**: {paper['date'].strftime('%Y-%m-%d')}\n"
        results_md += f"  - **摘要**: {paper['summary']}\n\n"
    
    return results_md

def generate_website_section(articles, category_name):
    """生成网站文章部分"""
    if not articles:
        return f"## 📰 {category_name}\n\n未在指定时间范围和网站中找到相关内容。\n\n"
    
    results_md = f"## 📰 {category_name}\n\n"
    
    # 按来源分组
    sources = {}
    for article in articles:
        source = article['source']
        if source not in sources:
            sources[source] = []
        sources[source].append(article)
    
    for source, source_articles in sources.items():
        results_md += f"### 来自 {source}\n"
        for article in source_articles:
            results_md += f"- **[{article['title']}]({article['url']})**\n"
            results_md += f"  - **发布日期**: {article['date'].strftime('%Y-%m-%d')}\n"
            results_md += f"  - **摘要**: {article['summary']}\n\n"
    
    return results_md