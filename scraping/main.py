# Scraper import
from scraper import Scraper

# Converter import (docling)
from docling_converter.converter import Converter

# Paths import (docling)
from docling_converter.docs.raw.doc_paths import DOC_URL_PATHS
from docling_converter.docs.raw.doc_paths import DOC_LOCAL_PATHS

class Main:

    def file_path_convertion(self):
        converter= Converter(path="")

        markdown_data= converter.doc_converter_by_file_path(DOC_LOCAL_PATHS)
        convertion_counter= 0

        if markdown_data:
            convertion_counter += 1
            converter.save_to_markdown(markdown_data, output_dir="docling_converter/docs/converted", filename=f"pdf_file_converted_{convertion_counter}")


    def url_file_convertion(self):
        converter= Converter(path="")

        markdown_data= converter.doc_converter_by_url(DOC_URL_PATHS)
        convertion_counter= 0

        if markdown_data:
            convertion_counter += 1
            converter.save_to_markdown(markdown_data, output_dir="docling_converter/docs/converted", filename=f"pdf_url_converted_{convertion_counter}")


    def html_convertion(self):
        scrape = Scraper()
        html_contents = scrape.fetch_data()
        converter = Converter(path="")

        for i, html in enumerate(html_contents):
            markdown_data = converter.doc_converter_by_html(html)
            if markdown_data:
                converter.save_to_markdown(markdown_data, output_dir="docling_converter/docs/converted", filename=f"html_converted_{i+1}")

if __name__ == "__main__":
    main = Main()
    # main.html_convertion()
    main.file_path_convertion()
    # main.url_file_convertion()