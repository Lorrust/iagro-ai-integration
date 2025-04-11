# Scraper import
from scraper import Scraper

# Converter import (docling)
from docling_converter.converter import Converter

# Paths import (docling)
from docling_converter.docs.raw.doc_paths import DOC_URL_PATHS
from docling_converter.docs.raw.doc_paths import DOC_LOCAL_PATHS

class Main:

    def __init__(self):
        self.converter = Converter(path="")
        self.scraper = Scraper()

    def file_path_convertion(self):
        converted_files = self.converter.convert_local_pdf_to_markdown(DOC_LOCAL_PATHS)

        for filename, markdown_data in converted_files:
            self.converter.save_to_markdown(
                data=markdown_data,
                output_dir="docling_converter/docs/converted",
                filename=filename
            )


    def url_file_convertion(self):
        converted_files= self.converter.convert_url_pdf_to_markdown(DOC_URL_PATHS)

        for filename, markdown_data in converted_files:
            self.converter.save_to_markdown(
                data=markdown_data,
                output_dir="docling_converter/docs/converted",
                filename=filename
            )


    def html_convertion(self):
        html_contents = self.scraper.fetch_data()

        for i, html in enumerate(html_contents):
            markdown_data = self.converter.convert_html_to_markdown(html, doc_id= i+1)

            if markdown_data:
                self.converter.save_to_markdown(markdown_data, output_dir="docling_converter/docs/converted", filename=f"html_converted_{i+1}")

if __name__ == "__main__":
    main = Main()
    main.html_convertion()
    main.file_path_convertion()
    main.url_file_convertion()