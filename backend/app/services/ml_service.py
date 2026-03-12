import os
import joblib
import numpy as np
from fastapi import HTTPException

MODEL_PATH = "app/ml_models/respiratory_risk_model.pkl"

class MLService:
    def __init__(self):
        self.model = None
        self._load_model()

    def _load_model(self):
        """Loads the pre-trained model if it exists."""
        if os.path.exists(MODEL_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
            except Exception as e:
                print(f"Error loading model: {e}")
        else:
            print("Model file not found. Predictions will be unavailable.")

    def predict_risk(self, health_data: dict, breath_data: dict, aqi_exposure: float) -> dict:
        """
        Predict respiratory risk using the loaded ML model.
        Returns a specific message if model is not available.
        """
        if self.model is None:
            return {
                "status": "unavailable",
                "message": "Prediction unavailable. ML model not trained yet.",
                "lung_health_score": None,
                "respiratory_risk_level": "Unknown",
                "probability_of_respiratory_disease": None
            }
        
        # Note: This feature mapping is illustrative until model is actually trained
        # In a real scenario, map inputs exactly to how the model was trained
        try:
            features = np.array([[
                health_data['age'],
                health_data['bmi'],
                1 if health_data['smoking_history'] else 0,
                breath_data['lung_capacity_score'],
                breath_data['breath_stability_score'],
                aqi_exposure
            ]])
            
            # Assuming a classifier predicting probablity of disease 
            probability = self.model.predict_proba(features)[0][1]
            health_score = max(0, min(100, 100 - (probability * 100)))
            
            if probability > 0.6: risk_level = "High"
            elif probability > 0.3: risk_level = "Medium"
            else: risk_level = "Low"
            
            return {
                "status": "success",
                "message": "Prediction successful.",
                "lung_health_score": round(health_score, 2),
                "respiratory_risk_level": risk_level,
                "probability_of_respiratory_disease": round(probability, 4)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Prediction error: {e}")

ml_service = MLService()
