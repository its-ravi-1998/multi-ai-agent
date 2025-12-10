from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter()



class ChatRequest(BaseModel):
    """Schema for chat request."""
    message: str = Field(..., description="User's chat message")


@router.post("/")
async def chat_endpoint(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """Protected chat endpoint - requires authentication."""
    return {
        "response": "Chat slave not implemented yet.",
        "user": current_user.email,
        "message": chat_request.message
    }


@router.get("/history")
async def get_chat_history(
    current_user: User = Depends(get_current_user)
):
    """Get chat history for the current user."""
    return {
        "history": "Chat history not implemented yet.",
        "user": current_user.email
    }