import os
import tempfile
from pathlib import Path
from datetime import datetime
from docling.document_converter import DocumentConverter

class Converter:
    def __init__(self, path: str):
        self.path = path
        self.converter = DocumentConverter()

    def doc_converter_by_url(self, url_paths: list) -> dict:
        """
        Convert a document to MD format.
        Args:
            url (str): URL of the document.
        Returns:
            dict: Converted document in MD format.
        """
        source = url_paths # PDF URLs list
        if not source:
            print("No URLs found!")
            return None

        print("Searching files...")
        url_files_converted = []
        
        try:

            for url in source:
                if source[url]:
                    print(f"File {source[url]} found!")
                    print("Converting files...")
                    result = self.converter.convert(source)

                    print("File converted successfully!")

                    converted_file = result.document.export_to_markdown()
                    url_files_converted.append(converted_file)
                
            print("File not found!")
            return None
        except Exception as e:
            print(f"Error while converting file: {e}")
            return None
    
    def doc_converter_by_file_path(self, local_paths: list) -> dict:
        """
        Convert a document to MD format.
        Args:
            path (str): Path to the document.
        Returns:
            dict: Converted document in MD format.
        """

        print("Searching files...")
        converted_files = []

        try:
            for path in local_paths:
                source = Path(path) # PDF path directory

                if not source.exists():
                    print("File not found!")
                    return None

                print(f"File {source} found!")
                print("Convertin file...")
                   
                
                result = self.converter.convert(source)

                converted_file = result.document.export_to_markdown()
                print("File converted successfully!")

                converted_files.append(converted_file)
        
        except Exception as e:
            print(f"Error while converting file: {e}")
            return None
    
    def doc_converter_by_html(self, html: str) -> dict:
        # HTML returned from the scraper
        """
        Convert a document to MD format.
        Args:
            html (str): HTML content of the document.
        Returns:
            dict: Converted document in MD format.
        """
        if not html:
            print("HTML content is empty!")
            return None

        print("Converting HTML content...")

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode='w', encoding='utf-8') as tmp_file:
                tmp_file.write(html)
                tmp_path = Path(tmp_file.name)
            
            result = self.converter.convert(tmp_path)
            converted_file = result.document.export_to_markdown()
            print("HTML content converted successfully!")

            if tmp_path.exists():
                os.remove(tmp_path)
            
            return converted_file
        
        except Exception as e:
            print(f"Error while converting HTML: {e}")
            return None
    
    def save_to_markdown(self, data: str, output_dir: str, filename: str = None) -> None:
        """
        Save the converted data to a MD file inside a specific directory.
        Args:
            data (str): Converted data in MD format.
            output_dir (str): Directory to save the file.
            filename (str, optional): Name of the file. If not provided, a timestamp will be used.
        """
        # Create the output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Generate a name for the file if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"converted_{timestamp}"

        filepath = os.path.join(output_dir, f"{filename}.md")

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(data)

            print(f"Markdown file saved in: {filepath}")
        except Exception as e:
            print(f"Error to save: {e}")
        