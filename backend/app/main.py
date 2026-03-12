from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.errors import setup_error_handlers
from app.core.rate_limit import setup_rate_limiting

app = FastAPI(
    title="Breathometer 4.0 Backend",
    description="Real-time backend API for Breathometer 4.0 health assessment platform.",
    version="1.0.0"
)

setup_error_handlers(app)
setup_rate_limiting(app)

# Configure CORS for real-time frontend dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Breathometer 4.0 Backend API"}

from app.routes import auth, environment, health, breath, prediction, ai, chatbot, reports, inference_api, alerts

# Routers will be included here as they are developed
app.include_router(auth.router)
app.include_router(environment.router)
app.include_router(health.router)
app.include_router(breath.router)
app.include_router(prediction.router)
app.include_router(ai.router)
app.include_router(chatbot.router)
app.include_router(reports.router)
app.include_router(inference_api.router)
app.include_router(alerts.router)

