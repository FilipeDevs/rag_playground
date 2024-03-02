import os
from utils.embeddings import get_emmbeddings_api
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from dotenv import load_dotenv
from .database import chunks_collection, db, alt_messages_collection
from models import Chunk

load_dotenv()


MONGO_URI = os.getenv("MONGO_URI")
ATLAS_VECTOR_SEARCH_INDEX_NAME = os.getenv("ATLAS_VECTOR_SEARCH_INDEX_NAME")


def insert_chunks_to_vector_db(document_chunks, file_id: str):
    for doc_chunk in document_chunks:
        emebedding = get_emmbeddings_api().embed_query(doc_chunk.page_content)
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
        f"{db.name} . {alt_messages_collection.name}",
        get_emmbeddings_api(),
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    )

    return vector_search_connection


def get_relevant_docs(question: str, file_ids: list[str]):

    pre_filter = {"source": {"$in": file_ids}}

    results = get_vector_db().similarity_search_with_score(
        query=question, k=5, pre_filter=pre_filter
    )

    if len(results) == 0 or results[0][1] < 0.75:
        print(f"Unable to find matching results.")
        return None

    return format_relevant_docs(results)


def format_relevant_docs(docs):
    context_text = "\n\n".join([doc.page_content for doc, _score in docs])

    return context_text
