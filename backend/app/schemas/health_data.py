from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class HealthDataCreate(BaseModel):
    age: int = Field(..., gt=0, lt=120)
    height: float = Field(..., description="Height in cm")
    weight: float = Field(..., description="Weight in kg")
    smoking_history: bool
    activity_level: str = Field(..., description="Low, Moderate, High")
    respiratory_symptoms: Optional[str] = None
    baseline_symptoms: Optional[str] = None

class HealthDataResponse(HealthDataCreate):
    id: str
    user_id: str
    bmi: float
    created_at: datetime

    class Config:
        from_attributes = True
