import os
import json
from pathlib import Path
from datetime import datetime
from docling.document_converter import DocumentConverter

#Variable that contains all the url to convert
from docs.raw.doc_paths import DOC_PATHS

class Converter:
    def __init__(self, path: str):
        self.path = path
        self.converter = DocumentConverter()

    def doc_converter_by_url(self, url: str) -> dict:
        """
        Convert a document to JSON format.
        Args:
            url (str): URL of the document.
        Returns:
            dict: Converted document in JSON format.
        """
        source = DOC_PATHS  # PDF URL
        print("Searching files...")

        for url in range(len(source)):
            if source[url]:
                print(f"File {source[url]} found!")
                print("Converting files...")
                result = self.converter.convert(source)

                print("File converted successfully!")

                converted_file = result.document.export_to_dict()
                return converted_file
            
        print("File not found!")
        return None
    
    def doc_converter_by_file_path(self, path: str) -> dict:
        """
        Convert a document to JSON format.
        Args:
            path (str): Path to the document.
        Returns:
            dict: Converted document in JSON format.
        """
        source = Path(path)  # PDF path directory
        print("Searching file...")

        if not source.exists():
            print("File not found!")
            return None

        print(f"File {source} found!")
        print("Converting file...")

        result = self.converter.convert(source)

        converted_file = result.document.export_to_dict()
        print("File converted successfully!")

        return converted_file
    
    def doc_converter_by_html(self, html: str) -> dict:
        # HTML returned from the scraper
        """
        Convert a document to JSON format.
        Args:
            html (str): HTML content of the document.
        Returns:
            dict: Converted document in JSON format.
        """
        if not html:
            print("HTML content is empty!")
            return None

        print("Converting HTML content...")

        try:
            result = self.converter.convert(html, format="html")
            converted_file = result.document.export_to_dict()
            print("HTML content converted successfully!")
            return converted_file
        except Exception as e:
            print(f"Error while converting HTML: {e}")
            return None
    
    def save_to_json(self, data: dict, output_dir: str, filename: str = None) -> None:
        """
        Save the converted data to a JSON file inside a specific directory.
        Args:
            data (dict): The data to save.
            output_dir (str): The directory to save the file in.
            filename (str): Optional filename (without extension). If not provided, uses timestamp.
        """
        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Generate a name for the file if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"converted_{timestamp}"

        filepath = os.path.join(output_dir, f"{filename}.json")

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"File saved in: {filepath}")
        except Exception as e:
            print(f"Error to save: {e}")
        