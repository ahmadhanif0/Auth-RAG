from fastapi import APIRouter
from rag.chat_chain import get_rag_chain

chat_router = APIRouter()


@chat_router.post("/chat/")
async def chat(query: str):

    rag_chain = get_rag_chain()

    response = rag_chain(query)

    return {
        "answer": response["answer"]
    }