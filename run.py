#!/usr/bin/env python
"""
Simple script to run the FastAPI application.
Usage: python run.py
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=8000,
        reload=True
    )

