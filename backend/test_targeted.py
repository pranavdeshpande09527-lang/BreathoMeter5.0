import httpx, asyncio

BASE = "http://localhost:8000"

async def main():
    async with httpx.AsyncClient(timeout=15.0) as c:
        # Test signup with a fresh email
        print("=== SIGNUP (fresh email) ===")
        r = await c.post(f"{BASE}/auth/signup", json={
            "email": "uniquetest303@breathometer.com",
            "password": "Test1234!",
            "full_name": "Unique Test"
        })
        print(f"Status: {r.status_code}")
        print(f"Body: {r.text}")
        
        # Test signup with already-used email (should be handled)
        print("\n=== SIGNUP (duplicate email) ===")
        r = await c.post(f"{BASE}/auth/signup", json={
            "email": "uniquetest303@breathometer.com",
            "password": "Test1234!",
            "full_name": "Duplicate"
        })
        print(f"Status: {r.status_code}")
        print(f"Body: {r.text}")

        # Test login with unconfirmed email
        print("\n=== LOGIN (unconfirmed) ===")
        r = await c.post(f"{BASE}/auth/login", json={
            "email": "uniquetest303@breathometer.com",
            "password": "Test1234!"
        })
        print(f"Status: {r.status_code}")
        print(f"Body: {r.text}")

        # Test each protected endpoint individually
        for name, method, url in [
            ("Health POST", "POST", f"{BASE}/health/input"),
            ("Breath POST", "POST", f"{BASE}/breath/test"),
            ("Predict POST", "POST", f"{BASE}/prediction/predict-risk"),
            ("AI POST", "POST", f"{BASE}/ai/explanation"),
            ("Chatbot POST", "POST", f"{BASE}/chatbot/message"),
            ("Report GET", "GET", f"{BASE}/reports/summary"),
            ("Profile GET", "GET", f"{BASE}/auth/profile"),
        ]:
            print(f"\n=== {name} (no auth) ===")
            if method == "GET":
                r = await c.get(url)
            else:
                r = await c.post(url, json={})
            print(f"Status: {r.status_code}")
            print(f"Body (first 200): {r.text[:200]}")

asyncio.run(main())
