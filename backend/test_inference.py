from fastapi.testclient import TestClient
from app.main import app
from app.core.dependencies import get_current_user

# Override auth dependency for testing
app.dependency_overrides[get_current_user] = lambda: {"user_id": "test_user"}

client = TestClient(app)

data = {
    "environmental_data": {
        "AQI": 600.0,
        "PM10": 80.0,
        "PM2_5": 55.0,
        "NO2": 40.0,
        "SO2": 20.0,
        "O3": 35.0,
        "Temperature": 30.0,
        "Humidity": 75.0,
        "WindSpeed": 5.0,
        "RespiratoryCases": 10.0,
        "CardiovascularCases": 5.0,
        "HospitalAdmissions": 2.0,
        "HealthImpactScore": 85.0
    },
    "optional_patient_data": {
        "age": 45,
        "condition": "asthma"
    }
}

response = client.post("/inference/predict", json=data)
print("Status Code:", response.status_code)
print("Response JSON:")
import json
try:
    print(json.dumps(response.json(), indent=2))
except Exception:
    print(response.text)
