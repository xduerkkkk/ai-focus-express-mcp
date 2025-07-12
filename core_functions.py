import arxiv
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import json
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse as parse_date # 强大的日期解析库
from web_utils import search_arxiv_papers, search_website_articles
from report_generator import generate_arxiv_section, generate_website_section


def load_sources():
    with open('sources.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def search_arxiv(keywords: str, time_limit: datetime, max_results=4):
    """搜索ArXiv论文"""
    print(f"正在搜索 ArXiv，关键词: {keywords}")
    papers = search_arxiv_papers(keywords, time_limit, max_results)
    return generate_arxiv_section(papers)

def search_websites(keywords: str, sources_list: list, category_name: str, time_limit: datetime):
    """搜索网站文章"""
    print(f"正在搜索 {category_name}...")
    articles = search_website_articles(keywords, sources_list, time_limit)
    return generate_website_section(articles, category_name)
def get_ai_focus_express(keywords: str, time_range: str = "过去一周") -> str:
    if not keywords:
        return "请输入要搜索的关键词。"

    # 计算起始时间点
    days_map = {"过去24小时": 1, "过去一周": 7, "过去一月": 30}
    delta_days = days_map.get(time_range, 7)
    # 设定一个明确的带时区的时间点
    time_limit = datetime.now(timezone.utc) - timedelta(days=delta_days)
    
    sources = load_sources()
    
    # 依次调用各个搜索模块
    arxiv_results = search_arxiv(keywords, time_limit)
    blog_results = search_websites(keywords, sources['tech_blogs'], "技术博客", time_limit)
    news_results = search_websites(keywords, sources['news_sites'], "行业新闻", time_limit)

    final_report = f"# AI焦点速递: “{keywords}”\n(时间范围: {time_range})\n\n"
    final_report += arxiv_results
    final_report += blog_results
    final_report += news_results
    
    return final_report