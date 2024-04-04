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
