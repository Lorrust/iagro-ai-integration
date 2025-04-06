from fastapi import APIRouter
from app.schemas.chat import ChatRequest, ChatResponse
from app.services import openai_service # TODO: Implement firebase_service

router = APIRouter()

@router.post("/diagnose", response_model=ChatResponse)
async def diagnose(request: ChatRequest):
    """
    Endpoint that receives a message and an optional image, processes the message,
    and returns the AI's response.
    """

    # If contains image:
    # image_url = None
    # if request.image:
    #     image_url = await firebase_service.upload_image(request.image)

    response = await openai_service.ask_ai(request)
    return response
