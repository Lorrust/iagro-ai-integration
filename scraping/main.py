# Scraper import
from scraper import Scraper

# Converter import (docling)
from docling_converter.converter import Converter

# Paths import (docling)
from docling_converter.docs.raw.doc_paths import DOC_URL_PATHS
from docling_converter.docs.raw.doc_paths import DOC_LOCAL_PATHS

class Main:

    """
    A main class to orchestrate the document conversion process.

    This class integrates the `Scraper` and `Converter` to:
    - Convert local PDF files to Markdown.
    - Convert PDF files from URLs to Markdown.
    - Convert HTML content to Markdown.
    - Save the converted files in the specified output directory.
    """

    def __init__(self):
        """
        Initializes the Main class with instances of the Converter and Scraper.
        """
        self.converter = Converter(path="")
        self.scraper = Scraper()

    def file_path_convertion(self):
        """
        Converts local PDF files to Markdown and saves the results.

        Uses the `DOC_LOCAL_PATHS` list to locate the files, converts them to Markdown,
        and saves the converted files in the `docling_converter/docs/converted` directory.
        """
        converted_files = self.converter.convert_local_pdf_to_markdown(DOC_LOCAL_PATHS)

        for filename, markdown_data in converted_files:
            self.converter.save_to_markdown(
                data=markdown_data,
                output_dir="docling_converter/docs/converted",
                filename=filename #Another filename for converted files? Change it here.
            )


    def url_file_convertion(self):
        """
        Converts PDF files from URLs to Markdown and saves the results.

        Uses the `DOC_URL_PATHS` list to fetch the files, converts them to Markdown,
        and saves the converted files in the `docling_converter/docs/converted` directory.
        """
        converted_files= self.converter.convert_url_pdf_to_markdown(DOC_URL_PATHS)

        for filename, markdown_data in converted_files:
            self.converter.save_to_markdown(
                data=markdown_data,
                output_dir="docling_converter/docs/converted",
                filename=filename #Another filename for converted files? Change it here.
            )


    def html_convertion(self):
        """
        Converts HTML content fetched by the Scraper to Markdown and saves the results.

        Fetches HTML content using the `Scraper`, converts it to Markdown,
        and saves the converted files in the `docling_converter/docs/converted` directory.
        """
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