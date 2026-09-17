import os
import shutil
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile # pyright: ignore[reportMissingImports]
from loguru import logger # pyright: ignore[reportMissingImports]

from config.config import settings
from services.document_processor import DocumentProcessor
from services.vector_store import store

router = APIRouter()

UPLOAD_DIR = Path("uploaded_documents")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload/")
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