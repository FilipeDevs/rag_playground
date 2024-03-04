from database import chunks_collection
from langchain_core.documents import Document


def get_chunks_from_file(file_id: str):
    documents_chunk = []

    chunks = chunks_collection.find({"source": file_id}, {"embedding": 0})
    for chunk in chunks:
        text = chunk.pop("text")
        documents_chunk.append(Document(page_content=text, metadata=chunk))

    return documents_chunk


def get_chunks_from_files_as_docs(file_ids: list[str]) -> list[Document]:
    documents_chunks = []
    for file_id in file_ids:
        documents_chunks += get_chunks_from_file(file_id)
    return documents_chunks
