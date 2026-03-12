import requests

url = "http://localhost:8000/auth/signup"
data = {
    "email": "testuser99@example.com",
    "password": "Password123",
    "full_name": "Test User",
    "role": "patient"
}

response = requests.post(url, json=data)
print(f"Status Code: {response.status_code}")
try:
    print(f"Error:\n{response.json()['detail']}")
except:
    print(f"Response: {response.text}")
