from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def chat_endpoint(message: str):
    return {"response": "Chat slave not implemented yet."}
