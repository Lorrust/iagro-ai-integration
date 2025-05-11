from app.services.chroma import client
from app.constants.chroma import COLLECTION_NAME

collection = client.get_collection(name=COLLECTION_NAME)

def get_relevant_context(query: str, k: int = 3) -> dict:
    """
    Retrieves relevant context from the ChromaDB collection based on the provided query.

    Args:
        query (str): The query text to search for in the knowledge base.
        k (int): The number of results to return.

    Returns:
        dict: A dictionary containing the documents, ids, metadata, and distances of the most relevant results.
    """
    results = collection.query(query_texts=[query], n_results=k)

    if results and results.get("documents") and results["documents"][0]:
        formatted_results = {
            "documents": results["documents"][0],
            "ids": results.get("ids", [[]])[0],
            "metadatas": results.get("metadatas", [[]])[0],
            "distances": results.get("distances", [[]])[0]
        }
        return formatted_results
    return {}
