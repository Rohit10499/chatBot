from fastapi import APIRouter
from pydantic import BaseModel
from app.services.retrieval_service import answer_question

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/ask")
async def ask_question(request: QueryRequest):
    return answer_question(request.question)
