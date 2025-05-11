from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services import openai_service

router = APIRouter()

@router.post("/diagnose", response_model=ChatResponse)
async def diagnose(request: ChatRequest) -> ChatResponse:
    """
    Endpoint that receives a ChatRequest and returns the AI's response.

    Args:
        request (ChatRequest): The request containing the message, optional image URL, message history, and context flag.

    Returns:
        ChatResponse: The AI's response containing the diagnosis or information requested.
    """
    response = await openai_service.ask_ai(request)
    return response
