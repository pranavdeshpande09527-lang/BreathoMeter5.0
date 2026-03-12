import os
import json
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv("c:\\Users\\prana\\.gemini\\antigravity\\scratch\\breathometer4-backend\\.env")

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

try:
    # try to select 1 row
    res = supabase.table("risk_predictions").select("*").limit(1).execute()
    print("risk_predictions schema/data:")
    if res.data:
        print(json.dumps(res.data[0], indent=2))
    else:
        print("No rows, but query succeeded.")
except Exception as e:
    print("Error querying risk_predictions:")
    print(e)

try:
    # try to select 1 row from breath_tests
    res = supabase.table("breath_tests").select("*").limit(1).execute()
    print("\nbreath_tests schema/data:")
    if res.data:
        print(json.dumps(res.data[0], indent=2))
    else:
        print("No rows, but query succeeded.")
except Exception as e:
    print("Error querying breath_tests:")
    print(e)
