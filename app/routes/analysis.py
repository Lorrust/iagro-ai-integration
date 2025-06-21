from fastapi import APIRouter
from app.services import openai_service
from app.schemas.analysis import AnalysisRequest, AnalysisResponse

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: AnalysisRequest):
    response = await openai_service.analyze(request)
    return response
