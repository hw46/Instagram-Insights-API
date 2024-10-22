from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi.responses import JSONResponse
from app.routers import insights
from app.core.config import limiter as app_limiter

app = FastAPI(
    title="Instagram Insights API",
    description="A FastAPI service to retrieve and analyze Instagram Insights data.",
    version="1.0.0",
)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# Include the insights router
app.include_router(insights.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Instagram Insights API!"}
