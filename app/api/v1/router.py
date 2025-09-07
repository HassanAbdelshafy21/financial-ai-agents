from fastapi import APIRouter
from .health import router as health_router
from .auth import router as auth_router
from .chats import router as chats_router  # Add this import

router = APIRouter()
router.include_router(health_router, prefix="/health", tags=["health"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(chats_router, prefix="/chats", tags=["chats"])  # Add this line