import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime
import time

class Scrapper:
    def __init__(self, url: str):
        """Initialize scrapper with The Hindu URL"""
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {e}")
            self.text = None
            return

        self.text = response.text
        self.soup = BeautifulSoup(self.text, 'html.parser')

    def get_editorial_links(self, num_articles: int = 1):
        """Find editorial links on the page"""
        if not self.text:
            return []

        editorial_links = []
        seen_links = set()

        # Find editorial links - look for links with strong tags and specific patterns
        for link in self.soup.find_all('a', href=True):
            href = link['href']
            
            if ('opinion/editorial/' in href and 
                href != 'https://www.thehindu.com/opinion/editorial/' and
                '/article' in href and 
                link.find('strong')):  
                
                # Make sure it's a full URL
                if not href.startswith('http'):
                    href = 'https://www.thehindu.com' + href
                
                if href not in seen_links:
                    seen_links.add(href)
                    editorial_links.append(href)
                    if len(editorial_links) >= num_articles:
                        break

        return editorial_links[:num_articles]

    def get_article_title(self):
        """Extract article title"""
        if not self.text:
            return "Title not found"
        
        title_tag = self.soup.find('h1')
        if title_tag:
            return title_tag.get_text().strip()
        
        meta_title = self.soup.find('meta', property='og:title')
        if meta_title and meta_title.get('content'):
            return meta_title.get('content').strip()
        
        return "Title not found"

    def get_article_content(self):
        """Extract clean article content, filtering out metadata and related topics"""
        if not self.text:
            return "Article content not found."

        # Find main content div
        content_div = self.soup.find('div', id=re.compile(r'^content-body-'))
        
        if not content_div:
            return "Article content could not be extracted."

        # Remove unwanted sections (related topics, metadata, etc.)
        for unwanted in content_div.find_all(['div', 'section', 'aside'], 
                                           class_=re.compile(r'(related|topic|tag|category|meta)', re.IGNORECASE)):
            unwanted.decompose()
        
        # Find all paragraphs and filter them
        paragraphs = content_div.find_all('p')
        filtered_paragraphs = []
        
        for p in paragraphs:
            text = p.get_text().strip()
            
            # Skip empty paragraphs
            if not text:
                continue
            
            # Skip category/tag lists (multiple forward slashes)
            if text.count('/') > 2:
                continue
            
            # Skip paragraphs with too many links (likely metadata)
            links = p.find_all('a')
            if links and len(links) > 2:
                link_text_length = sum(len(a.get_text().strip()) for a in links)
                total_text_length = len(text)
                
                if total_text_length > 0 and (link_text_length / total_text_length) > 0.7:
                    continue
            
            filtered_paragraphs.append(text)
        
        return '\n'.join(filtered_paragraphs)
    

    def scrape_articles(self, num_articles: int = 1) -> str:
        
        editorial_links = self.get_editorial_links(num_articles=num_articles)
        
        if not editorial_links:
            return json.dumps({
                'status': 'error',
                'message': 'No editorial links found',
                'articles': [],
                'scraped_at': datetime.now().isoformat()
            }, indent=2, ensure_ascii=False)
        
        articles_data = []
        
        for idx, link in enumerate(editorial_links, 1):
            try:
                # Create new scrapper instance for each article
                article_scrapper = Scrapper(link)
                
                article_data = {
                    'article_number': idx,
                    'url': link,
                    'title': article_scrapper.get_article_title(),
                    'content': article_scrapper.get_article_content(),
                    'status': 'success'
                }
                
                articles_data.append(article_data)
                
                
                time.sleep(0.5)
                
            except Exception as e:
                articles_data.append({
                    'article_number': idx,
                    'url': link,
                    'title': 'Error occurred',
                    'content': f'Failed to scrape article: {str(e)}',
                    'status': 'error'
                })
        
        result = {
            'status': 'success',
            'total_articles': len(articles_data),
            'scraped_at': datetime.now().isoformat(),
            'articles': articles_data
        }
        
        return json.dumps(result, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # Example usage - scrape 1 editorial by default
    url = "https://www.thehindu.com/opinion/editorial/"
    scrapper = Scrapper(url)
    
    
    result = scrapper.scrape_articles(num_articles=3)
    print(result)
    
