import os
import json
import tempfile
from pathlib import Path
from datetime import datetime

#Docling library
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    AcceleratorDevice,
    AcceleratorOptions,
    PdfPipelineOptions,
)
from docling.datamodel.settings import settings
from docling.document_converter import DocumentConverter, PdfFormatOption

# Docling Chunker
from transformers import AutoTokenizer
from docling.chunking import HybridChunker

# Utils
from scraping.utils.data_cleaning import clean_text

class Converter:

    """
    A class for converting documents (PDFs, HTML, etc.) into Markdown format and processing them into smaller chunks.

    This class uses the Docling library to handle document conversion and chunking. It supports:
    - Converting local PDF files to Markdown.
    - Converting PDF files from URLs to Markdown.
    - Converting HTML content to Markdown.
    - Splitting documents into smaller chunks for further processing.
    - Saving converted documents and chunks in Markdown or JSON format.

    Attributes:
        path (str): The path to the document or directory to be processed.
        accelerator_options (AcceleratorOptions): Options for configuring the processing accelerator (e.g., CPU or GPU).
        pipeline_options (PdfPipelineOptions): Options for configuring the PDF processing pipeline.
        converter (DocumentConverter): The Docling document converter instance used for processing documents.
    """

    def __init__(self, path: str):
        self.path = path
        self.accelerator_options = AcceleratorOptions(
            num_threads=8, device=AcceleratorDevice.CPU
        )
        self.pipeline_options = PdfPipelineOptions()
        self.pipeline_options.accelerator_options = self.accelerator_options
        self.pipeline_options.do_ocr = True
        self.pipeline_options.do_table_structure = True
        self.pipeline_options.table_structure_options.do_cell_matching = True

        settings.debug.profile_pipeline_timings = True

        self.converter = DocumentConverter(
            format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options= self.pipeline_options,
            )
        }
        )



    def convert_url_pdf_to_markdown(self, url_paths: list, doc_id: int = 1) -> list:
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
        url_files_not_found = []

        try:
            for i, url in enumerate(url_paths, start=doc_id):
                if url:
                    print(f"File {url} found!")
                    print("Converting file...")

                    result = self.converter.convert(url)

                    if result:
                        chunks = self.chunker(result.document)

                        # Generate a base filename for the converted file
                        converted_filename = f"url_pdf_converted_{i}"
                        chunks_filename = f"url_pdf_chunks_{i}"

                        # Save chunks in JSON for RAG
                        self.save_chunks_to_json(
                            chunks=chunks,
                            output_dir="docling_converter/docs/rag_chunks",
                            filename=chunks_filename,
                            source=f"{converted_filename}.md"
                        )
                        print("Chunks saved successfully!")

                        converted_file = result.document.export_to_markdown()
                        url_files_converted.append((converted_filename, converted_file))

                        print("File converted successfully!")
                        doc_conversion_secs = result.timings["pipeline_total"].times
                        print(f"Conversion time: {doc_conversion_secs}")

                    else:
                        print(f"Failed to convert file: {url}")
                        url_files_not_found.append(url)

            return url_files_converted
        
        except Exception as e:
            print(f"Error while converting file: {e}")
            return None
        
        
        

    def convert_local_pdf_to_markdown(self, local_paths: list, doc_id: int = 1) -> list:
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
            for i, path in enumerate(local_paths, start=doc_id):
                source = Path(path)

                if not source.exists():
                    print(f"File not found: {source}")
                    continue

                print(f"File {source} found!")
                print("Converting file...")

                result = self.converter.convert(source)

                if result:
                    chunks = self.chunker(result.document)

                    converted_filename = f"local_pdf_converted_{i}"
                    chunks_filename = f"local_pdf_chunks_{i}"

                    # Save chunks in JSON for RAG
                    self.save_chunks_to_json(
                        chunks=chunks,
                        output_dir="docling_converter/docs/rag_chunks",
                        filename=chunks_filename,
                        source=f"{converted_filename}.md"
                    )
                    print("Chunks saved successfully!")

                    converted_file = result.document.export_to_markdown()
                    doc_conversion_secs = result.timings["pipeline_total"].times
                    print(f"Conversion time: {doc_conversion_secs}")

                    converted_files.append((converted_filename, converted_file))
                    print("File converted successfully!")

            return converted_files

        except Exception as e:
            print(f"Error while converting file: {e}")
            return None
    
    def convert_html_to_markdown(self, html: str, doc_id: int = 1) -> str:
        # HTML returned from the scraper
        """
        Convert a document to MD format.
        Args:
            html (str): HTML content of the document.
            doc_id (int): Document ID for chunking.
        Returns:
            str: Converted document in MD format.
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
            
            if result:
                chunks= self.chunker(result.document)

                # Save chunks in JSON for RAG
                self.save_chunks_to_json(
                    chunks=chunks,
                    output_dir="docling_converter/docs/rag_chunks",
                    filename=f"html_chunks_{doc_id}",
                    source=f"html_converted_{doc_id}.md"
                )
                print("Chunks saved successfully!")

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

    def chunker(self, doc , chunk_size: int = 460) -> list:
        """
        Split the data into smaller chunks removing not needed characters from docuemnt text.
        Args:
            doc (Document): Docling Document to be split.
            chunk_size (int): Size of each chunk.
        Returns:
            list: List of chunks.
        """
        EMBED_MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
        MAX_TOKENS = chunk_size

        tokenizer = AutoTokenizer.from_pretrained(EMBED_MODEL_ID, truncation= True, padding=True)
        tokenizer.model_max_length = 512
        
        chunker = HybridChunker(
            tokenizer=tokenizer,
            max_tokens=MAX_TOKENS,
            merge_peers=True,
        )

        chunker_iter= chunker.chunk(dl_doc= doc)
        chunks= list(chunker_iter)

         # Verificar e truncar se necessário
        for chunk in chunks:
            tokens = tokenizer.encode(chunk.text)
            if len(tokens) > 512:
                print(f"Warning: Chunk exceeds max length: {len(tokens)}")
                chunk.text = tokenizer.decode(tokens[:512])  # Truncar os tokens para 512

        print(f"Total number of chunks: {len(chunks)}")
        return chunks
    
    def save_chunks_to_json(self, chunks, output_dir: str, filename: str, source: str = None):
        """
        Save chunks in JSON format, ready for use in RAG.

        Args:
            chunks (list): Chunks list (objects with `.text`).
            output_dir (str): Directory the archive will be saved.
            filename (str): JSON archive name.
            source (str): (Optional) original document identifier.
        """
        os.makedirs(output_dir, exist_ok=True)

        chunk_data = []
        for i, chunk in enumerate(chunks):
            chunk_entry = {
                "text": clean_text(chunk.text).strip(),
                "metadata": {
                    "chunk_index": i,
                    "tokens": len(chunk.text.split()),
                    "source": source or "unknown"
                }
            }
            chunk_data.append(chunk_entry)

        json_path = os.path.join(output_dir, f"{filename}.json")

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(chunk_data, f, ensure_ascii=False, indent=2)

        print(f"Chunks saved in: {json_path}")