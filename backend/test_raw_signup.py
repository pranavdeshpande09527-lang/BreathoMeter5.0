import asyncio
from app.database import supabase_auth_request

async def test_signup():
    print("Testing normal signup...")
    try:
        resp = await supabase_auth_request("signup", "POST", {
            "email": "standard_user2@example.com",
            "password": "Password123",
            "data": {"role": "patient"}
        })
        print(resp)
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(test_signup())
