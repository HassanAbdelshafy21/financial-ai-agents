from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.agent import agent
from app.api.v1.health import router as health_router  # <-- import at top
from app.api.v1.auth import router as auth_router  # <-- import at top


# Add proper prefix so the route becomes /api/v1/agent/query
router = APIRouter()
router.include_router(health_router, prefix="/health", tags=["health"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])


# Define the request schema
class QueryRequest(BaseModel):
    query: str
    thread_id: str = "default"


# Endpoint: POST with JSON body
@router.post("/query")
async def query_agent(request: QueryRequest):
    result = agent.invoke({"messages": [("user", request.query)]}, config={"configurable": {"thread_id": request.thread_id}})
    # Extract the final message
    final_message = result["messages"][-1].content if "messages" in result else result
    return {"answer": final_message}
