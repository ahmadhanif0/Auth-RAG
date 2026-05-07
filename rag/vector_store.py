from langchain_chroma import Chroma
from rag.embedding import embeddings


VECTOR_DB_PATH = "chroma_db"


def store_chunks_in_vector_db(chunks):

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH
    )

    return vector_store