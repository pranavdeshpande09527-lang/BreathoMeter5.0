from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from app.core.database import get_db
from app.core.dependencies import get_current_user, get_authenticated_db
from app.core.rate_limit import limiter
import logging

router = APIRouter(prefix="/prediction", tags=["prediction"])
logger = logging.getLogger(__name__)

from typing import List, Optional

class PredictionRequest(BaseModel):
    final_risk_score: float = 0.0
    risk_category: str
    ai_explanation: str
    top_risk_factors: List[str]

@router.post("/store")
@limiter.limit("10/minute")
async def store_prediction(request: Request, data: PredictionRequest, user = Depends(get_current_user), supabase = Depends(get_authenticated_db)):
    user_id = user.id
    
    try:
        res = supabase.table("risk_predictions").insert({
            "user_id": user_id,
            "final_risk_score": data.final_risk_score,
            "predicted_condition": data.risk_category,  # map risk_category to predicted_condition for backwards compatibility if needed, or simply let risk_category save directly
            "risk_category": data.risk_category,
            "ai_explanation": data.ai_explanation,
            "top_risk_factors": data.top_risk_factors
        }).execute()
        
        return {"message": "Prediction saved successfully", "data": res.data[0] if res.data else {}}
    except Exception as e:
        logger.error(f"Error storing prediction: {e}")
        raise HTTPException(status_code=500, detail="Failed to store risk prediction")

@router.get("/{user_id_param}")
@limiter.limit("10/minute")
async def get_prediction_history(request: Request, user_id_param: str, user = Depends(get_current_user), supabase = Depends(get_authenticated_db)):
    user_id = user.id
    if user_id_param != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    try:
        res = supabase.table("risk_predictions").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        return res.data
    except Exception as e:
        logger.error(f"Error fetching predictions for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch prediction history")
