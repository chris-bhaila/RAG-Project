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

app = FastAPI()

@app.get("/")
def health_check():
    return {"message": "API is running!"}

@app.post("/chat", response_model=ChatResponse)
async def chatbot(request: chatbotInputRequest):
    start_time = time.perf_counter()
    retrieval_docs = store.retrieve_docs(request.question, k=3)
    augmented_messages = augment_messages(request.question, retrieval_docs)
    llm = model_provider.chatmodel(model_name=settings.CHAT_MODEL, temp=0.6)
    llm_response = llm.invoke(augmented_messages)

    end_time = time.perf_counter()
    logger.info(f"Chatbot response time: {end_time - start_time:.2f} seconds")

    return ChatResponse(
        answer=llm_response.content,
        response_time=round(end_time - start_time, 2),
        latency=str(round(end_time - start_time, 2))
    )

#Create a directory to store uploaded documents
UPLOAD_DIR = Path("uploaded_documents")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    # 1. (Optional) Restrict file types
    allowed_extensions = {".pdf", ".docx", ".txt", ".csv"}
    file_extension = Path(file.filename).suffix.lower()
   
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
        )
 
    # 2. Define the target file path
    file_path = UPLOAD_DIR / file.filename

    files = os.listdir(UPLOAD_DIR)
    if files:
        logger.info("Cleaning up the upload directory before saving the new file.")
        for existing_file in files:
            relative_path = os.path.join(UPLOAD_DIR, existing_file)
            abs_path = os.path.abspath(relative_path)
            os.remove(abs_path)
 
    # 3. Stream and save the file to disk
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks = DocumentProcessor.load_and_split_documents(file_path)
    store.create_vector_store(chunks, settings.VECTOR_STORE)
 
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "saved_path": str(file_path),
        "status": "successfully uploaded"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", port=settings.PORT, reload=settings.ENV)