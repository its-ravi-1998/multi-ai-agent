import uvicorn
from time import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.routers import chat, auth


# Create FastAPI app
app = FastAPI(title="Multi Agent API")


# Middleware: Request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time()
    response = await call_next(request)
    duration = round(time() - start, 4)
    print(f"{request.method} {request.url.path} completed_in={duration}s status_code={response.status_code}")
    return response


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])


# Root endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)