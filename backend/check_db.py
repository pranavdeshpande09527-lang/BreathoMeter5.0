import asyncio
from app.core.database import get_db

async def check():
    supabase = get_db()
    
    # Get total count of predictions
    pred_res = supabase.table("risk_predictions").select("*", count="exact").execute()
    print("Predictions count:", pred_res.count)
    if pred_res.data:
        print("Latest prediction:", pred_res.data[0])

    # Get total count of breath tests
    breath_res = supabase.table("breath_tests").select("*", count="exact").execute()
    print("Breath tests count:", breath_res.count)
    if breath_res.data:
        print("Latest breath test:", breath_res.data[0])

if __name__ == "__main__":
    asyncio.run(check())
