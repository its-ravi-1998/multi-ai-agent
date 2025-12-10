from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.agents.intent_detection_agent import intent_detection_agent
from app.utils.auth import get_current_user
from app.models.user import User
from app.schema.intent import IntentResponse

router = APIRouter()

class DetectIntentRequest(BaseModel):
    message: str = Field(..., description="User's message")

@router.post("/", response_model=IntentResponse)
async def detect_intent(request: DetectIntentRequest, current_user: User = Depends(get_current_user)):
    intent, confidence = await intent_detection_agent(request.message)
    return IntentResponse(name=intent, confidence=confidence)