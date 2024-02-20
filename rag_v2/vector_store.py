from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from config.database import file_collection
from config.database import ATLAS_VECTOR_SEARCH_INDEX_NAME
from rag_v2.hugo_embedding import hugging_api_embeddings
from config.database import MONGO_URI


def create_vector_store(docs):
    vector_store = MongoDBAtlasVectorSearch.from_documents(
        documents=docs,
        embedding=hugging_api_embeddings,
        collection=file_collection,
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    )

    return vector_store


def vector_search_connection():
    vector_search_connection = MongoDBAtlasVectorSearch.from_connection_string(
        MONGO_URI,
        "document_db" + "." + "document_chunks",
        hugging_api_embeddings,
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    )

    return vector_search_connection
