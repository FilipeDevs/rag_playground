import os
from dotenv import load_dotenv
from config.database import DatabaseManager
from utils.embeddings import get_emmbeddings_api
from langchain_community.vectorstores import MongoDBAtlasVectorSearch

load_dotenv()

chunk_collection = DatabaseManager.chunks_collection
db_name = DatabaseManager.db_name
chunk_collection_name = chunk_collection.name


def insert_to_vector_db(document_chunks):
    """
    Insert document chunks to the vector database, along with their embeddings,
    and some metadata.
    """
    for doc_chunk in document_chunks:
        emebedding = get_emmbeddings_api().embed_query(doc_chunk.page_content)
        metadata = doc_chunk.metadata
        chunk_data = {
            "source": metadata["source"],
            "page_number": metadata["page"],
            "text": doc_chunk.page_content,
            "embedding": emebedding,
        }

        chunk_collection.insert_one(chunk_data)


def get_vector_db():
    """
    Instantiate the vector database and return it.
    """
    vector_db = MongoDBAtlasVectorSearch.from_connection_string(
        os.getenv("MONGO_URL"),
        f"{db_name}.{chunk_collection_name}",
        get_emmbeddings_api(),
        index_name=os.getenv("ATLAS_VECTOR_SEARCH_INDEX_NAME"),
    )

    return vector_db
