import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("breathometer")

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected server error occurred."},
    )

async def auth_exception_handler(request: Request, exc: Exception):
    logger.error(f"Authentication failure: {exc}")
    # Will be triggered for specific auth exceptions we define or JWT failure
    return JSONResponse(
        status_code=401,
        content={"detail": str(exc)},
    )
    
def setup_error_handlers(app):
    app.add_exception_handler(Exception, global_exception_handler)
    # FastApi handles HTTPException natively, but we can override if needed
