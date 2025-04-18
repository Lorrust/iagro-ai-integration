import json
from pathlib import Path
from app.services.chroma import indexer

DOCS_FOLDER = Path("scraping/docling_converter/docs/converted")

def extract_text_from_docling(doc_json: dict) -> str:
    """
    Extracts text from a Docling JSON document.

    Args:
        doc_json (dict): The JSON representation of the Docling document.

    Returns:
        str: The extracted text from the document.
    """
    texts = doc_json.get("texts", [])
    return "\n".join(text.get("text", "") for text in texts if "text" in text)

def load_documents() -> list[dict]:
    """
    Loads documents from a fixed folder and extracts their text content.

    Returns:
        list[dict]: A list of dictionaries containing the title and content of each document.
    """
    docs = []
    for file in DOCS_FOLDER.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            content = extract_text_from_docling(data)
            title = data.get("name", file.stem)
            docs.append({"title": title, "content": content})
    return docs

if __name__ == "__main__":
    documents = load_documents()
    indexer.index_documents(documents)
    print(f"Indexed {len(documents)} documents into ChromaDB.")
