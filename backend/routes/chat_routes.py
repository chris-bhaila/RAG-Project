import time
from fastapi import APIRouter # pyright: ignore[reportMissingImports]
from services.vector_store import store
from schemas.response import ChatResponse
from schemas.requests import chatbotInputRequest
from loguru import logger # pyright: ignore[reportMissingImports]
from config.config import settings
from utils.util import augment_messages
from services.models import model_provider

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
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