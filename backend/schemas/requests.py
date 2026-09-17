from pydantic import BaseModel

class chatbotInputRequest(BaseModel):
    question: str