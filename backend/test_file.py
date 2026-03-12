import httpx, asyncio

BASE = "http://localhost:8000"
lines = []

async def t(name, method, url, json_data=None, expect=None):
    try:
        async with httpx.AsyncClient(timeout=15.0) as c:
            r = await c.request(method, url, json=json_data)
            ok = (r.status_code == expect) if expect else True
            mark = "PASS" if ok else "FAIL"
            lines.append(f"{mark} | {name} | got={r.status_code} exp={expect} | {r.text[:150]}")
    except Exception as e:
        lines.append(f"FAIL | {name} | ERROR: {e}")

async def main():
    await t("Root", "GET", f"{BASE}/", expect=200)
    await t("AQI", "GET", f"{BASE}/environment/aqi?location=here", expect=200)
    await t("Weather", "GET", f"{BASE}/environment/weather?lat=21.15&lon=79.09", expect=200)
    await t("AQI Map", "GET", f"{BASE}/environment/aqi-map?location=here", expect=200)
    await t("Signup", "POST", f"{BASE}/auth/signup", json_data={"email":"filetest@breathometer.com","password":"Test1234!","full_name":"FT"}, expect=200)
    await t("Login unconfirmed", "POST", f"{BASE}/auth/login", json_data={"email":"filetest@breathometer.com","password":"Test1234!"}, expect=403)
    await t("Health no auth", "POST", f"{BASE}/health/input", json_data={"age":25,"height":175.0,"weight":70.0,"smoking_history":False,"activity_level":"Moderate"}, expect=401)
    await t("Breath no auth", "POST", f"{BASE}/breath/test", json_data={"durations":[15.2],"attempt_count":1}, expect=401)
    await t("Predict no auth", "POST", f"{BASE}/prediction/predict-risk", expect=401)
    await t("AI no auth", "POST", f"{BASE}/ai/explanation", json_data={"topic":"test","user_context":{}}, expect=401)
    await t("Chatbot no auth", "POST", f"{BASE}/chatbot/message", json_data={"message":"hi","user_context":{}}, expect=401)
    await t("Report no auth", "GET", f"{BASE}/reports/summary", expect=401)
    await t("Profile no auth", "GET", f"{BASE}/auth/profile", expect=401)
    await t("Health Latest no auth", "GET", f"{BASE}/health/latest", expect=401)
    await t("Breath Latest no auth", "GET", f"{BASE}/breath/latest", expect=401)
    
    with open("test_out.txt", "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
        passed = sum(1 for l in lines if l.startswith("PASS"))
        failed = sum(1 for l in lines if l.startswith("FAIL"))
        f.write(f"\nTOTAL: {passed} passed, {failed} failed\n")

asyncio.run(main())
