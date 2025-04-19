from app.services.chroma import client

collection = client.get_collection(name="knowledge-base")

def get_relevant_context(query: str, k: int = 3) -> list[str]:
    """
    Retrieves relevant context from the ChromaDB collection based on the provided query.

    Args:
        query (str): The query text to search for in the knowledge base.
        k (int): The number of results to return.

    Returns:
        list[str]: A list of relevant documents from the knowledge base.
    """
    results = collection.query(query_texts=[query], n_results=k)
    return results["documents"][0] if results["documents"] else []
