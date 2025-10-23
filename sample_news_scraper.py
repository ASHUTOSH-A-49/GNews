import requests
from bs4 import BeautifulSoup

def scrape_toi_news(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    
    articles = []
    
    list_container = soup.find('div', class_='articlelist')
    if not list_container:
        list_container = soup.find('div', class_='main-content')
    
    if not list_container:
        return []
        
    story_links = list_container.find_all('a') 

    for link_tag in story_links:
        title = link_tag.text.strip()
        link = link_tag.get('href')
        
        if title and link and len(title) > 20 and not link.endswith('/videos'):
            if not link.startswith('http'):
                link = 'https://timesofindia.indiatimes.com' + link
            
            summary = "Follow link for details."
            
            article = {
                'title': title,
                'link': link,
                'summary': summary
            }
            articles.append(article)
            
    return articles

def print_results(articles):
    if not articles:
        print("No articles were scraped.")
        return
    
    print(f"\n--- Scraped {len(articles)} Times of India Articles ---")
    for i, article in enumerate(articles):
        print(f"[{i + 1}] {article['title']}")
        print(f"    Link: {
