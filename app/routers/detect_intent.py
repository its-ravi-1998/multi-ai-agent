from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from app.agents.intent_detection_agent import intent_detection_agent
from app.utils.auth import get_current_user
from app.models.user import User
from app.schema.intent import IntentResponse
from app.models.intent import Intent
from app.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

class DetectIntentRequest(BaseModel):
    message: str = Field(..., description="User's message")

@router.post("/", response_model=IntentResponse)
async def detect_intent(request: DetectIntentRequest, db: AsyncSession = Depends(get_db)):
    intent, confidence = await intent_detection_agent(request.message)
    intent_model = Intent(name=intent, confidence=confidence, raw_input=request.message)
    db.add(intent_model)
    await db.commit()
    await db.refresh(intent_model)
    return IntentResponse(name=intent_model.name, confidence=intent_model.confidence)