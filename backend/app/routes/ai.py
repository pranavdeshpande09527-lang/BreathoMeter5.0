from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.ai_service import ai_service
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/ai", tags=["AI Explanations"])

class ExplanationRequest(BaseModel):
    topic: str
    user_context: Optional[dict] = {}

class ExplanationResponse(BaseModel):
    explanation: str

@router.post("/explanation", response_model=ExplanationResponse)
async def get_explanation(request: ExplanationRequest, user = Depends(get_current_user)):
    explanation = await ai_service.generate_explanation(request.topic, request.user_context)
    return {"explanation": explanation}
