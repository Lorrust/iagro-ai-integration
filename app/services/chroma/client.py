from chromadb import PersistentClient

_chroma_client = PersistentClient(path="./chroma_db")

def get_chroma_client():
    """
    Returns the Chroma client instance for executing queries.
    """
    return _chroma_client
