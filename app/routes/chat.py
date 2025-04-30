from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services import openai_service
from app.services.chroma.chroma_service import chroma_service

router = APIRouter()

@router.post("/diagnose", response_model=ChatResponse)
async def diagnose(request: ChatRequest):
    """
    Endpoint that receives a message and an optional image, processes the message,
    and returns the AI's response.

    Args:
        request (ChatRequest): The request containing the message and, optionally, an image URL.

    Returns:
        ChatResponse: The AI's response containing the diagnosis.
    """

    # Search for relevant context in the Chroma knowledge base
    chroma_results = chroma_service.query_chroma(request.message)

    # Calls the OpenAI service with the request and the results from Chroma
    response = await openai_service.ask_ai(request, chroma_results)

    return response
