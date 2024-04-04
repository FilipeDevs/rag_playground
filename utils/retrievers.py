from database import get_vector_db
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever


from utils import (
    get_chunks_from_files_as_docs,
    get_logger,
)

from utils.formatters import (
    format_chunks_as_context,
    get_ids_from_chunks_without_score,
    format_relevant_chunks_with_score,
    get_ids_from_chunks,
)

logger = get_logger()


def get_vector_db_as_retriever(file_ids: list[str]):
    return get_vector_db().as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5, "pre_filter": {"source": {"$in": file_ids}}},
    )


def get_bm25_retriever(file_ids: list[str]):
    candidate_chunks = get_chunks_from_files_as_docs(file_ids)
    bm25_retriever = BM25Retriever.from_documents(documents=candidate_chunks)
    bm25_retriever.k = 3
    return bm25_retriever


def get_ensemble_retriever(vector_embeddings_retriever, bm25_retriever):
    return EnsembleRetriever(
        retrievers=[vector_embeddings_retriever, bm25_retriever], weights=[0.5, 0.5]
    )


def get_relevant_context(query: str, file_ids: list[str]):
    vector_retriever = get_vector_db_as_retriever(file_ids)
    bm25_retriever = get_bm25_retriever(file_ids)

    ensemble_retriever = get_ensemble_retriever(vector_retriever, bm25_retriever)

    docs = ensemble_retriever.get_relevant_documents(query=query)
    chunks_ids = get_ids_from_chunks_without_score(docs)

    return (format_chunks_as_context(docs), chunks_ids)


def get_relevant_chunks_with_score(query: str, file_ids: list[str]):
    pre_filter = {"source": {"$in": file_ids}}
    results = get_vector_db().similarity_search_with_score(
        query=query, k=7, pre_filter=pre_filter
    )

    if len(results) == 0 or results[0][1] < 0.75:
        logger.warning("No relevant chunks found")
        return None

    formatted_results = format_relevant_chunks_with_score(results)
    chunks_ids = get_ids_from_chunks(results)

    return formatted_results, chunks_ids
