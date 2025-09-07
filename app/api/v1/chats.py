from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.auth.dependencies import get_current_user
from app.models import User, Chat, Message
from sqlalchemy.future import select
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List

# Pydantic schemas for API responses
class ChatResponse(BaseModel):
    id: int
    title: str
    thread_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class CreateChatRequest(BaseModel):
    title: str

router = APIRouter()

# Try writing a simple GET /chats endpoint that returns the current user's chats
@router.get("/", response_model=List[ChatResponse])
async def get_user_chats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    chats = await db.execute(
        select(Chat).filter(Chat.user_id == current_user.id)
    )
    return chats.scalars().all()
# Try writing a simple POST /chats endpoint that creates a new chat for the current user
@router.post("/", response_model=ChatResponse)
async def create_chat(
    request: CreateChatRequest,  # Changed this
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Need to generate a unique thread_id and create Chat object
    import uuid
    thread_id = str(uuid.uuid4())
    
    new_chat = Chat(
        title=request.title,
        user_id=current_user.id,
        thread_id=thread_id
    )
    db.add(new_chat)
    await db.commit()
    await db.refresh(new_chat)
    return new_chat

# Try writing a simple GET /chats/{chat_id}/messages endpoint that returns messages for a chat
@router.get("/{chat_id}/messages", response_model=List[MessageResponse])
async def get_chat_messages(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # First check if chat belongs to user
    chat = await db.get(Chat, chat_id)
    if not chat or chat.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    messages = await db.execute(
        select(Message).filter(Message.chat_id == chat_id)
    )
    return messages.scalars().all()
@router.delete("/{chat_id}", response_model=dict)
async def delete_chat(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    chat = await db.get(Chat, chat_id)
    if not chat or chat.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Chat not found")
    await db.delete(chat)
    await db.commit()
    return {"detail": "Chat deleted"}
class SaveMessageRequest(BaseModel):
    role: str
    content: str

@router.post("/{chat_id}/messages")
async def save_message(
    chat_id: int,
    request: SaveMessageRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verify chat belongs to user
    chat = await db.get(Chat, chat_id)
    if not chat or chat.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    # Create and save message
    new_message = Message(
        chat_id=chat_id,
        role=request.role,
        content=request.content
    )
    db.add(new_message)
    await db.commit()
    return {"message": "Message saved"}
