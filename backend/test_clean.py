import httpx, asyncio, json, sys

BASE = "http://localhost:8000"

async def t(name, method, url, json_data=None, headers=None, expect=None):
    try:
        async with httpx.AsyncClient(timeout=15.0) as c:
            r = await c.request(method, url, json=json_data, headers=headers)
            ok = (r.status_code == expect) if expect else True
            body = r.text[:200].replace("\n", " ")
            mark = "PASS" if ok else "FAIL"
            line = f"{mark} | {name} | got={r.status_code} exp={expect} | {body}"
            print(line, flush=True)
            return ok
    except Exception as e:
        print(f"FAIL | {name} | ERROR: {e}", flush=True)
        return False

async def main():
    r = []
    r.append(await t("Root", "GET", f"{BASE}/", expect=200))
    r.append(await t("AQI", "GET", f"{BASE}/environment/aqi?location=here", expect=200))
    r.append(await t("Weather", "GET", f"{BASE}/environment/weather?lat=21.15&lon=79.09", expect=200))
    r.append(await t("AQI Map", "GET", f"{BASE}/environment/aqi-map?location=here", expect=200))
    r.append(await t("Signup", "POST", f"{BASE}/auth/signup", json_data={"email":"fix202@breathometer.com","password":"Test1234!","full_name":"Fix"}, expect=200))
    r.append(await t("Login unconfirmed", "POST", f"{BASE}/auth/login", json_data={"email":"fix202@breathometer.com","password":"Test1234!"}, expect=403))
    r.append(await t("Health no auth", "POST", f"{BASE}/health/input", json_data={"age":25,"height":175.0,"weight":70.0,"smoking_history":False,"activity_level":"Moderate"}, expect=401))
    r.append(await t("Breath no auth", "POST", f"{BASE}/breath/test", json_data={"durations":[15.2],"attempt_count":1}, expect=401))
    r.append(await t("Predict no auth", "POST", f"{BASE}/prediction/predict-risk", expect=401))
    r.append(await t("AI no auth", "POST", f"{BASE}/ai/explanation", json_data={"topic":"test","user_context":{}}, expect=401))
    r.append(await t("Chatbot no auth", "POST", f"{BASE}/chatbot/message", json_data={"message":"hi","user_context":{}}, expect=401))
    r.append(await t("Report no auth", "GET", f"{BASE}/reports/summary", expect=401))
    r.append(await t("Profile no auth", "GET", f"{BASE}/auth/profile", expect=401))
    r.append(await t("Health Latest no auth", "GET", f"{BASE}/health/latest", expect=401))
    r.append(await t("Breath Latest no auth", "GET", f"{BASE}/breath/latest", expect=401))
    
    passed = sum(1 for x in r if x)
    failed = sum(1 for x in r if not x)
    print(f"TOTAL: {passed} passed, {failed} failed", flush=True)

asyncio.run(main())
