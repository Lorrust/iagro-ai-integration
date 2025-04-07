from scraper import fetch_data
from docling_converter.converter import Converter
class Scraper:
    # def __init__(self, url):
    #     self.url = url

    # def scrape(self):
    #     pass

    # def converter(self):
    #     pass

    def test(self):
        html_contents = fetch_data()
        converter = Converter(path="")  # path pode ser vazio para HTML

        for i, html in enumerate(html_contents):
            json_data = converter.doc_converter_by_html(html)
            if json_data:
                converter.save_to_json(json_data, output_dir="docling_converter/docs/converted", filename=f"html_converted_{i+1}")

if __name__ == "__main__":
    scraper = Scraper()
    # scraper.scrape()
    # scraper.converter()
    scraper.test()