from fastapi import FastAPI
from app.api.v1.router import router as v1_router
from app.core.logging import setup_logging, logger
from app.core.config import settings
from app.agents.router import router as agent_router

# Setup logging
setup_logging()

app = FastAPI(title="Financial AI Agents API", version="0.0.1")

# Include the main v1 API router
app.include_router(v1_router, prefix="/api/v1")


@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Financial AI Agents API - use /api/v1/health"}


# Debug endpoint to verify the OpenAI API key being used
@app.get("/debug/openai-key")
def debug_openai_key():
    return {"OPENAI_API_KEY": settings.OPENAI_API_KEY}


# Include agent routes with correct versioning
app.include_router(agent_router, prefix="/api/v1")
