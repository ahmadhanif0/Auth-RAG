from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text_into_chunks(text: str):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.create_documents([text])

    return chunks