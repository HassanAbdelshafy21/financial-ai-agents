from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.agent import agent
from .auth import router as auth_router        # <-- move to top
from .health import router as health_router    # <-- move to top


router = APIRouter()
router.include_router(health_router, prefix="/health", tags=["health"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])


class QueryRequest(BaseModel):
    query: str


@router.post("/query")
async def query_agent(request: QueryRequest):
    result = agent.invoke({"messages": [("user", request.query)]})
    final_message = (
        result["messages"][-1].content if "messages" in result else result
    )
    return {"answer": final_message}
