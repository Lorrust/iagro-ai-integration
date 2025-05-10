from app.services.chroma.client import get_chroma_client
from app.services.embeddings.generator import get_text_embeddings
from app.models.knowledge_document import KnowledgeDocument

class ChromaService:

    def __init__(self):
        self.client = get_chroma_client()
        self.collection = self.client.get_or_create_collection(name="knowledge-base")

    def add_document(self, document: KnowledgeDocument):
        """
        Adds a document to the ChromaDB collection.

        Args:
            document (KnowledgeDocument): The document to be added.

        Returns:
            str: A message indicating the result of the operation.
        """
        embedding = get_text_embeddings(document.text)
        self.collection.add(
            documents=[document.text],
            embeddings=[embedding],
            metadatas=[document.metadata],
            ids=[document.id]
        )
        return f"Document {document.id} added successfully."

    def query_chroma(self, query_text: str, n_results: int = 5):
        """
        Queries the ChromaDB collection for relevant documents based on the provided text.

        Args:
            query_text (str): The text to query against the knowledge base.
            n_results (int): The number of results to return.

        Returns:
            List[KnowledgeDocument]: A list of documents that match the query.
        """
        query_embeddings = get_text_embeddings(query_text)
        results = self.collection.query(
            query_embeddings=query_embeddings.tolist(),
            n_results=n_results
    )
        return results

chroma_service = ChromaService()
