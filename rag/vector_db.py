import os
from database.database import file_collection
from rag.embeddings import hugging_api_embeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
ATLAS_VECTOR_SEARCH_INDEX_NAME = os.getenv("ATLAS_VECTOR_SEARCH_INDEX_NAME")


def create_vector_db(document_chunks, user_id):
    current_position = 0
    for chunk_id, doc_chunk in enumerate(document_chunks):
        end_position = current_position + len(doc_chunk.page_content)
        emebedding = hugging_api_embeddings.embed_query(
            doc_chunk.page_content)
        metadata = doc_chunk.metadata
        chunk_data = {
            "source": metadata["source"],
            "page_number": metadata["page"],
            "chunk_id": chunk_id,
            "text": doc_chunk.page_content,
            "embedding": emebedding,
            "start_position": current_position,
            "end_position": end_position,
            "user_id": user_id,  # Who the document belongs to
        }

        file_collection.insert_one(chunk_data)

        current_position = end_position


def vector_db():
    vector_search_connection = MongoDBAtlasVectorSearch.from_connection_string(
        MONGO_URI,
        "document_db" + "." + "document_chunks",
        hugging_api_embeddings,
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    )

    return vector_search_connection


def vector_db_v2(docs):
    vector_search = MongoDBAtlasVectorSearch.from_documents(
        documents=docs,
        collection=file_collection,
        embedding=hugging_api_embeddings,
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    )

    return vector_search
