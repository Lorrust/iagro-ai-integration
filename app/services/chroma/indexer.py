from app.services.chroma import client

collection = client.get_collection()

def index_documents(docs: list[dict]):
    """
    Indexes a list of documents into the ChromaDB collection.

    Args:
        docs (list[dict]): A list of documents to be indexed. Each document should be a dictionary
                           containing 'content' and 'title'.
    """
    for i, doc in enumerate(docs):
        collection.add(
            documents=[doc["content"]],
            metadatas=[{"source": doc["title"]}],
            ids=[f"doc_{i}"]
        )
