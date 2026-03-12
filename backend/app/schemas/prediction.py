from pydantic import BaseModel
from datetime import datetime

class PredictionResponse(BaseModel):
    id: str
    user_id: str
    lung_health_score: float
    respiratory_risk_level: str
    probability_of_respiratory_disease: float
    created_at: datetime
    
    class Config:
        from_attributes = True
