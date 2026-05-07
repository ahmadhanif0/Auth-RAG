from langchain_core.prompts import ChatPromptTemplate
from rag.retriever import get_retriever
from rag.llm import llm


def get_rag_chain():

    retriever = get_retriever()

    prompt = ChatPromptTemplate.from_template("""
    You are a helpful assistant.

    Use ONLY this context to answer:

    {context}

    Question: {question}
    """)

    def format_docs(docs):
        return "\n\n".join([doc.page_content for doc in docs])

    def rag_chain(question: str):

        docs = retriever.invoke(question)

        context = format_docs(docs)

        messages = prompt.format_messages(
            context=context,
            question=question
        )

        response = llm.invoke(messages)

        return {
            "answer": response.content,
            "context": context
        }

    return rag_chain