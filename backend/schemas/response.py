from pydantic import BaseModel

class UploadResponse(BaseModel):
    filename: str
    content_type: str
    saved_path: str

class ChatResponse(BaseModel):
    answer: str
    response_time: float
    latency: str