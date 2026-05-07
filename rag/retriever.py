from langchain_chroma import Chroma
from rag.embedding import embeddings

VECTOR_DB_PATH = "chroma_db"


def load_vector_store():
    return Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )


def get_retriever():
    vector_store = load_vector_store()

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}  # top 4 chunks
    )

    return retriever