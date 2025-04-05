from scraping.scraper import Scraper
# from scraping.docling.converter import

class Scraper:
    def __init__(self, url):
        self.url = url

    def scrape(self):
        pass

    def converter(self):
        pass


if __name__ == "__main__":
    scraper = Scraper()
    scraper.scrape()
    scraper.converter()