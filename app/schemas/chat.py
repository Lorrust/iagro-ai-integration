from pydantic import BaseModel, HttpUrl
from typing import Optional

class ChatRequest(BaseModel):
    """
    Represents a request to the AI model for diagnosis.

    Attributes:
        message (str): The description of the problem.
        image_url (Optional[HttpUrl]): An optional URL to an image related to the problem.
    """
    message: str
    image_url: Optional[HttpUrl] = None

class ChatResponse(BaseModel):
    """
    Represents the response from the AI model.

    Attributes:
        categoria (str): "Doença | Praga | Deficiência Nutricional | Outro"
        tipo (str): The type of the diagnosis.
        descricao (str): A description of the diagnosis.
        recomendacao (str): Recommendations based on the diagnosis.
    """
    categoria: str
    tipo: str
    descricao: str
    recomendacao: str
