from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from app.routers import chat

app = FastAPI(title="Multi Agent API")


app.include_router(chat.router, prefix="/chat", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)