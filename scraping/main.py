import requests
from bs4 import BeautifulSoup
from config import BASE_URL

def fetch_data ():
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.prettify()
        else:
            raise Exception(f"Failed to fetch data from {BASE_URL}. Status code: {response.status_code}")
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"An error occurred while fetching data: {e}")

html_data= fetch_data()

print(f"Webscraping: {html_data}")
