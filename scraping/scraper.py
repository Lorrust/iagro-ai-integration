import requests
from bs4 import BeautifulSoup
from config import BASE_URL

def fetch_data():
    results = []
    for url in BASE_URL:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                html_data = soup.prettify()
                results.append(html_data)
            else:
                print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching data from {url}: {e}")
    print(len(results), "HTML files fetched successfully!")
    return results