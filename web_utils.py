# web_utils.py
import re
import json
import requests
import arxiv
from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_date
from datetime import timezone
from googlesearch import search

def extract_publish_date(soup):
    """增强的日期提取函数"""
    # 1. 标准的 <time> 标签
    time_tag = soup.find('time')
    if time_tag and time_tag.has_attr('datetime'):
        try:
            return parse_date(time_tag['datetime'], ignoretz=True).replace(tzinfo=timezone.utc)
        except:
            pass
    
    # 2. JSON-LD 结构化数据
    json_ld_scripts = soup.find_all('script', type='application/ld+json')
    for script in json_ld_scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, list):
                data = data[0]
            
            date_fields = ['datePublished', 'dateCreated', 'dateModified', 'publishedAt']
            for field in date_fields:
                if field in data:
                    return parse_date(data[field], ignoretz=True).replace(tzinfo=timezone.utc)
        except:
            continue
    
    # 3. Meta 标签
    meta_selectors = [
        'meta[property="article:published_time"]',
        'meta[name="publish_date"]',
        'meta[name="date"]',
        'meta[name="pubdate"]',
        'meta[property="og:published_time"]',
        'meta[name="article:published_time"]',
        'meta[name="DC.date.issued"]'
    ]
    
    for selector in meta_selectors:
        meta_tag = soup.select_one(selector)
        if meta_tag and meta_tag.get('content'):
            try:
                return parse_date(meta_tag['content'], ignoretz=True).replace(tzinfo=timezone.utc)
            except:
                continue
    
    # 4. 常见的 class 和 id 选择器
    date_selectors = [
        '.publish-date', '.publication-date', '.post-date', '.article-date',
        '.date-published', '.entry-date', '.blog-date', '.news-date',
        '#publish-date', '#publication-date', '#post-date',
        '[class*="date"]', '[class*="time"]', '[id*="date"]'
    ]
    
    for selector in date_selectors:
        elements = soup.select(selector)
        for element in elements:
            text = element.get_text().strip()
            if text and len(text) > 6:
                try:
                    date_patterns = [
                        r'\d{4}-\d{2}-\d{2}',
                        r'\d{2}/\d{2}/\d{4}',
                        r'\d{1,2}\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{4}',
                        r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*\s+\d{1,2},?\s+\d{4}',
                    ]
                    
                    for pattern in date_patterns:
                        match = re.search(pattern, text, re.IGNORECASE)
                        if match:
                            return parse_date(match.group(), ignoretz=True).replace(tzinfo=timezone.utc)
                except:
                    continue
    
    return None

def extract_title(soup, url):
    """提取页面标题"""
    title_selectors = [
        'h1.title', 'h1.post-title', 'h1.article-title', 'h1.entry-title',
        'h1', 'title', 'meta[property="og:title"]', 'meta[name="twitter:title"]'
    ]
    
    for selector in title_selectors:
        element = soup.select_one(selector)
        if element:
            if element.name == 'meta':
                title = element.get('content', '').strip()
            else:
                title = element.get_text().strip()
            
            if title and len(title) > 5:
                return title
    
    return url

def extract_content_summary(soup, max_length=300):
    """提取网页内容摘要"""
    # 移除不需要的元素
    for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'advertisement']):
        element.decompose()
    
    content_selectors = [
        'meta[name="description"]',
        'meta[property="og:description"]',
        '.article-content', '.post-content', '.entry-content', '.content',
        'article', 'main', '.main-content', '[role="main"]',
        'p'
    ]
    
    content_text = ""
    
    for selector in content_selectors:
        elements = soup.select(selector)
        if not elements:
            continue
            
        if selector.startswith('meta'):
            content_text = elements[0].get('content', '')
        else:
            if selector == 'p':
                paragraphs = elements[:5]
                content_text = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
            else:
                content_text = elements[0].get_text().strip()
        
        content_text = ' '.join(content_text.split())
        
        if len(content_text) > 50:
            break
    
    if len(content_text) > max_length:
        content_text = content_text[:max_length] + "..."
    
    return content_text or "未能提取到内容摘要"

def search_arxiv_papers(keywords, time_limit, max_results=4):
    """搜索ArXiv论文"""
    results = []
    try:
        search_client = arxiv.Search(
            query=keywords, 
            max_results=max_results, 
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        
        for result in search_client.results():
            if result.published.replace(tzinfo=timezone.utc) >= time_limit:
                title = result.title.replace('[', '\\[').replace(']', '\\]')
                authors = ', '.join(author.name for author in result.authors)
                results.append({
                    'title': title,
                    'url': result.pdf_url,
                    'authors': authors,
                    'date': result.published,
                    'summary': result.summary[:200] + "..." if len(result.summary) > 200 else result.summary
                })
    except Exception as e:
        print(f"搜索 ArXiv 时出错: {e}")
        return []
    
    return results

def search_website_articles(keywords, sources_list, time_limit):
    """搜索网站文章"""
    all_articles = []
    
    for source in sources_list:
        query = f'"{keywords}" site:{source["url"]}'
        print(f"  - 正在搜索 {source['name']}...")
        
        try:
            search_results_urls = list(search(query, num_results=2, lang="en"))
            
            for url in search_results_urls:
                result = get_page_content_and_date(url, time_limit)
                if result:
                    title, date, summary = result
                    all_articles.append({
                        'title': title,
                        'url': url,
                        'date': date,
                        'summary': summary,
                        'source': source['name']
                    })
        except Exception as e:
            print(f"  - Google搜索 {source['name']} 时出错: {e}")
    
    return all_articles

def get_page_content_and_date(url, time_limit):
    """获取页面内容和日期（更新为返回三个值）"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        publish_date = extract_publish_date(soup)
        if not publish_date:
            return None
            
        if publish_date >= time_limit:
            title = extract_title(soup, url)
            content_summary = extract_content_summary(soup)
            return title, publish_date, content_summary
            
    except Exception as e:
        print(f"  - 解析URL({url})时出错: {e}")
        return None
    
    return None