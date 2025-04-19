import requests
from bs4 import BeautifulSoup
from config import BASE_URL

class Scraper:
    """
    A web scraper class to fetch and process HTML content from a list of URLs.
    """
    
    def fetch_data(self):
        """
        Fetches HTML content from the URLs specified in the BASE_URL list.

        For each URL:
        - Sends an HTTP GET request.
        - Parses the HTML content using BeautifulSoup.
        - Removes empty tags from the HTML.
        - Collects the prettified HTML content.

        Returns:
            list: A list of prettified HTML strings fetched from the URLs.
        """
        
        results = []
        for url in BASE_URL:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Extract the HTML content
                    for tag in soup.find_all():
                        if not tag.get_text(strip=True):
                            tag.decompose()
                        
                    html_data = soup.prettify()
                    results.append(html_data)
                else:
                    print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"An error occurred while fetching data from {url}: {e}")
        print(len(results), "HTML files fetched successfully!")
        return results