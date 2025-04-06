from pydantic import BaseModel, HttpUrl
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    image_url: Optional[HttpUrl] = None

class ChatResponse(BaseModel):
    categoria: str
    tipo: str
    descricao: str
    recomendacao: str
