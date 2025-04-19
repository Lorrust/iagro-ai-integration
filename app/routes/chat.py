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

    # TODO: Verify if the image will be in base64 or URL format
    # If the request contains an image
    # image_url = None
    # if request.image:
    #     image_url = await firebase_service.upload_image(request.image)

    # Search for relevant context in the Chroma knowledge base
    chroma_results = chroma_service.query_chroma(request.message)

    # Calls the OpenAI service with the request and the results from Chroma
    response = await openai_service.ask_ai(request, chroma_results)

    return response
