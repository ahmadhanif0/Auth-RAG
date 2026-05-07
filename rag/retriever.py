from langchain_chroma import Chroma
from rag.embedding import embeddings
from models.file import File

VECTOR_DB_PATH = "chroma_db"


def load_vector_store():
    return Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )


async def get_active_file_id():
    active_file =  await File.filter(is_active=True).first()
    return active_file.id if active_file else None

def get_retriever(file_id: int):

    vector_store = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings,
        collection_name=f"file_{file_id}"
    )

    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )