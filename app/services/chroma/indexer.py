from app.services.chroma import client
from app.constants import COLLECTION_NAME

client = client.get_chroma_client()
collection = client.get_or_create_collection(name=COLLECTION_NAME)

def index_documents(docs: list[dict]):
    """
    Indexes a list of chunk documents into the ChromaDB collection.
    """
    collection.add(
        documents=[doc["content"] for doc in docs],
        metadatas=[doc["metadata"] for doc in docs],
        ids=[doc["id"] for doc in docs],
    )
