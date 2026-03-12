from pydantic import BaseModel
from typing import List
from datetime import datetime

class BreathTestCreate(BaseModel):
    durations: List[float]
    attempt_count: int

class BreathTestResponse(BaseModel):
    id: str
    user_id: str
    average_duration: float
    lung_capacity_score: float
    breath_stability_score: float
    breath_strength_index: float
    created_at: datetime
    
    class Config:
        from_attributes = True
