from pathlib import Path
import time
from schemas.response import ChatResponse
from services.document_processor import DocumentProcessor
from loguru import logger # pyright: ignore[reportMissingImports]
from schemas.requests import chatbotInputRequest
from fastapi import FastAPI, File, UploadFile, HTTPException  # pyright: ignore[reportMissingImports]
import uvicorn
from config.config import settings
import shutil
import os
from services.vector_store import store
from utils.util import augment_messages
from services.models import model_provider
from routes.chat_routes import router as chat_router
from routes.uploaded_route import router as upload_router

app = FastAPI(title="RAG Chatbot API")

@app.get("/")
def health_check():
    return {"message": "API is running!"}

app.include_router(chat_router, tags=["Chat"])
app.include_router(upload_router, tags=["Upload"])

if __name__ == "__main__":
    uvicorn.run("main:app", port=settings.PORT, reload=settings.ENV)