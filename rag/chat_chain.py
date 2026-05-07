from models.file import File
from rag.retriever import get_retriever
from rag.llm import llm


async def get_rag_chain():

    active_file = await File.filter(is_active=True).first()

    if not active_file:
        return None

    retriever = get_retriever(active_file.id)

    def rag_chain(question: str):

        docs = retriever.invoke(question)

        context = "\n\n".join([d.page_content for d in docs])

        response = llm.invoke([
            ("system", "Answer only from context"),
            ("human", f"Context:\n{context}\n\nQuestion:{question}")
        ])

        return {"answer": response.content}

    return rag_chain