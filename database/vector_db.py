import os
from utils import get_logger
from utils.embeddings_manager import get_embeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from dotenv import load_dotenv
from .database import chunks_collection, db
from models import Chunk

load_dotenv()

logger = get_logger()

MONGO_URI = os.getenv("MONGO_URI")
ATLAS_VECTOR_SEARCH_INDEX_NAME = os.getenv("ATLAS_VECTOR_SEARCH_INDEX_NAME")


def insert_chunks_to_vector_db(document_chunks, file_id: str):
    for doc_chunk in document_chunks:
        emebedding = get_embeddings().embed_query(doc_chunk.page_content)
        metadata = doc_chunk.metadata
        chunk = Chunk(
            source=str(file_id),
            page_number=metadata["page"],
            text=doc_chunk.page_content,
            embedding=emebedding,
        )

        chunks_collection.insert_one(dict(chunk))


def get_vector_db():
    vector_search_connection = MongoDBAtlasVectorSearch.from_connection_string(
        MONGO_URI,
        f"{db.name}.{chunks_collection.name}",
        get_embeddings(),
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    )

    return vector_search_connection


def get_vector_db_as_retriever(file_ids: list[str]):
    return get_vector_db().as_retriever(
        search_type="similarity",
        search_kwargs={"k": 7, "pre_filter": {"source": {"$in": file_ids}}},
    )


def get_relevant_chunks(query: str, file_ids: list[str]):

    pre_filter = {"source": {"$in": file_ids}}

    results = get_vector_db().similarity_search_with_score(
        query=query, k=10, pre_filter=pre_filter
    )

    if len(results) == 0 or results[0][1] < 0.75:
        logger.warning("No relevant chunks found")
        return None

    formatted_results = format_relevant_chunks(results)
    chunks_ids = get_ids_from_chunks(results)

    return formatted_results, chunks_ids


def format_relevant_chunks(chunks):
    context_text = "\n\n".join([chunk.page_content for chunk, _score in chunks])

    return context_text


def get_ids_from_chunks(chunks):
    return [str(chunk.metadata["_id"]) for chunk, _score in chunks]


def get_ids_from_chunks_without_score(chunks):
    return [str(chunk.metadata["_id"]) for chunk in chunks]
