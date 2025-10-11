import requests
from bs4 import BeautifulSoup
import re

class Scrapper:
    def __init__(self, url: str):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {e}")
            self.text = None
            return

        self.text = response.text
        self.soup = BeautifulSoup(self.text, 'html.parser')

    def get_latest_editorial_link(self):
        """
        Finds the link to the latest editorial on the page.
        It looks for an 'a' tag containing a 'strong' tag, which is a pattern
        for the main editorial link on the page.
        """
        if not self.text:
            return None

        # The user's example shows the link is inside a <strong> tag.
        # We find all 'a' tags and check if they contain a 'strong' tag and link to an editorial.
        for link in self.soup.find_all('a', href=True):
            if 'opinion/editorial/' in link['href'] and link.find('strong'):
                # Return the first link that matches the pattern
                return link['href']
        return None

    def get_article_content(self):
        """
        Extracts the content of the article.
        The main content is located in a div with an ID that starts with 'content-body-'.
        """
        if not self.text:
            return "Article content not found."

        # The article content is inside a div with a dynamic ID like 'content-body-12345'
        # We can use a regular expression to find this div.
        content_div = self.soup.find('div', id=re.compile(r'^content-body-'))
        
        if content_div:
            # Find all paragraphs within the content div and join them.
            paragraphs = content_div.find_all('p')
            return '\n'.join(p.get_text() for p in paragraphs)
        else:
            return "Article content could not be extracted."

def main():
    """
    Main function to scrape and print the latest editorial.
    """
    # Step 1: Scrape the main editorial page to find the latest article link
    editorial_page_url = 'https://www.thehindu.com/opinion/editorial/'
    print(f"Fetching editorial list from: {editorial_page_url}")
    client = Scrapper(url=editorial_page_url)
    latest_link = client.get_latest_editorial_link()

    if latest_link:
        # Step 2: Construct the full URL for the latest editorial
        if not latest_link.startswith('http'):
            latest_link = f"https://www.thehindu.com{latest_link}"
        
        print(f"Found latest editorial link: {latest_link}")

        # Step 3: Scrape the article page and extract the content
        print("Fetching article content...")
        article_client = Scrapper(url=latest_link)
        article_content = article_client.get_article_content()
        
        # Step 4: Print the extracted content
        print("\n--- LATEST EDITORIAL ---")
        print(article_content)
        print("------------------------\n")
    else:
        print("Could not find the latest editorial link.")

if __name__ == '__main__':
    main()

    

