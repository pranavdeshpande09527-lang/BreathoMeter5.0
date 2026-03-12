import requests
import json
import uuid

base_url = "http://localhost:8000"

random_num = uuid.uuid4().hex[:6]
email = f"test_{random_num}@example.com"
print(f"Signing up with {email}...")

signup_data = {"email": email, "password": "Password123", "full_name": "Test User", "role": "patient"}
resp = requests.post(f"{base_url}/auth/signup", json=signup_data)
token = resp.json().get("session", {}).get("access_token")

if not token:
    print("Failed to get token:", resp.json())
    exit(1)

headers = {"Authorization": f"Bearer {token}"}

# Test Breath API
print("\n--- Testing Breath API ---")
breath_payload = {
    "lung_capacity": 30.0,
    "breath_duration": 10.0,
    "breath_strength": 20.0,
    "test_accuracy": 95.0,
    "peak_airflow": 0.0,
    "signal_stability": 0.0,
    "is_valid": True,
    "background_noise_detected": False,
    "cough_detected": False,
    "raw_attempts": []
}
r1 = requests.post(f"{base_url}/breath-test", headers=headers, json=breath_payload)
print(r1.status_code)
print(r1.text)

# Test Prediction API
print("\n--- Testing Prediction API ---")
pred_payload = {
    "final_risk_score": 0.25,
    "risk_category": "Low Risk",
    "ai_explanation": "Test explanation.",
    "top_risk_factors": ["Test Factor"]
}
r2 = requests.post(f"{base_url}/prediction/store", headers=headers, json=pred_payload)
print(r2.status_code)
print(r2.text)
