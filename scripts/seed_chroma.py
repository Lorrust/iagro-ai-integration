import json
from pathlib import Path
from app.services.chroma import indexer

DOCS_FOLDER = Path("scraping/docling_converter/docs/rag_chunks")

def load_chunks() -> list[dict]:
    """
    Loads chunks from the fixed folder.
    Each chunk will be a separate document.
    """
    chunks = []
    for file in DOCS_FOLDER.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            chunk_list = json.load(f)
            source = file.stem
            for idx, chunk in enumerate(chunk_list):
                text = chunk.get("text", "")
                metadata = chunk.get("metadata", {})
                metadata["source"] = source
                chunks.append({
                    "id": f"{source}_chunk_{idx}",
                    "content": text,
                    "metadata": metadata
                })
    return chunks

def main():
    chunks = load_chunks()
    indexer.index_documents(chunks)
    print(f"Indexed {len(chunks)} chunks into ChromaDB.")
