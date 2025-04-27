from typing import Any
from fastapi import APIRouter
from app.services.chroma.client import get_chroma_client
from app.constants.chroma import COLLECTION_NAME
import random

router = APIRouter()

@router.get("/chroma/random")
async def get_random_document() -> dict:
    """
    Retrieves a random document from the ChromaDB collection.

    Returns:
        dict: A dictionary containing the id, document, and metadata of the random document.
    """
    client = get_chroma_client()
    collection = client.get_collection(name=COLLECTION_NAME)

    all_docs = collection.get()
    ids = all_docs.get("ids", [])
    documents = all_docs.get("documents", [])
    metadatas = all_docs.get("metadatas", [])

    if not ids:
        return {"message": "Nenhum documento encontrado."}

    random_index = random.randint(0, len(ids) - 1)

    return {
        "id": ids[random_index],
        "document": documents[random_index],
        "metadata": metadatas[random_index],
    }

@router.get("/chroma/all")
async def get_all_documents() -> dict[str, Any]:
    """
    Retrieves all documents from the ChromaDB collection.

    Returns:
        list[dict[str, str]]: A list of dictionaries containing the ids, documents, and metadata of all documents.
    """
    client = get_chroma_client()
    collection = client.get_collection(name=COLLECTION_NAME)

    all_docs = collection.get()
    return {
        "ids": all_docs.get("ids", []),
        "documents": all_docs.get("documents", []),
        "metadatas": all_docs.get("metadatas", []),
    }
