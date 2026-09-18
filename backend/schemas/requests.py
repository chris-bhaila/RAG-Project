from pydantic import BaseModel
from typing import List, Any

class chatbotInputRequest(BaseModel):
    question: List[dict[str, Any]]