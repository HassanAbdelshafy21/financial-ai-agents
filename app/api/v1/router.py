from fastapi import APIRouter
from .health import router as health_router
from .auth import router as auth_router
from .chats import router as chats_router  # Add this import
from .reports import router as reports_router


router = APIRouter()
router.include_router(health_router, prefix="/health", tags=["health"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(chats_router, prefix="/chats", tags=["chats"]) 
router.include_router(reports_router, prefix="/reports", tags=["reports"])