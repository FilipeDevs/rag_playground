from langchain_core.documents import Document


def format_chunks_as_context(chunks: list[Document]) -> str:
    return "\n\n".join([chunk.page_content for chunk in chunks])


def format_relevant_chunks_with_score(chunks: list[Document]):
    context_text = "\n\n".join([chunk.page_content for chunk, _score in chunks])

    return context_text


def get_ids_from_chunks_without_score(chunks: list[Document]):
    return [str(chunk.metadata["_id"]) for chunk in chunks]


def get_ids_from_chunks(chunks: list[Document]):
    return [str(chunk.metadata["_id"]) for chunk, _score in chunks]
