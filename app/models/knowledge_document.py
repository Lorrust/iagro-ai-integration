from pydantic import BaseModel
from typing import Optional, Dict

class KnowledgeDocument(BaseModel):
    """
    Represents a knowledge document to be stored in ChromaDB.

    Attributes:
        id (str): Unique identifier for the document.
        text (str): The content of the document.
        metadata (Optional[Dict[str, str]]): Optional metadata associated with the document.
    """
    id: str
    text: str
    metadata: Optional[Dict[str, str]] = {}

    class Config:
        """
        Pydantic configuration for the KnowledgeDocument model.
        """
        str_min_length = 1
        str_strip_whitespace = True
