from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional

class Message(BaseModel):
    """
    Represents a message in the chat.

    Attributes:
        role (str): The role of the message sender, either "user" or "assistant".
        content (str): The content of the message.
    """
    role: str = Field(..., enum=["user", "assistant"])
    content: str = Field(...)

class ChatRequest(BaseModel):
    """
    Represents a request to the AI model for diagnosis.

    Attributes:
        message (str): The description of the problem.
        image_url (Optional[HttpUrl]): An optional URL to an image related to the problem.
        message_history (Optional[List[Message]]): A list of previous messages in the conversation.
        use_context (Optional[bool]): A flag indicating whether to retrieve context from ChromaDB.
    """
    message: str
    image_url: Optional[HttpUrl] = None
    message_history: Optional[List[Message]] = None
    use_context: Optional[bool] = None

class ChatResponse(BaseModel):
    """
    Represents the response from the AI model.

    If the conversation has already started, only the `mensagem` field is used.

    Attributes:
        categoria (Optional[str]): "Doença | Praga | Deficiência Nutricional | Outro"
        tipo (Optional[str]): The type of the diagnosis.
        descricao (Optional[str]): A description of the diagnosis.
        recomendacao (Optional[str]): Recommendations based on the diagnosis.
        mensagem (Optional[str]): A message from the AI model, used for follow-up conversations.
    """
    titulo: Optional[str] = None
    categoria: Optional[str] = None
    tipo: Optional[str] = None
    descricao: Optional[str] = None
    recomendacao: Optional[str] = None
    mensagem: Optional[str] = None
