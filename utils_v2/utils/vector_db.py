import os
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from utils.embeddings import hugging_api_embeddings

from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
ATLAS_VECTOR_SEARCH_INDEX_NAME = os.getenv("ATLAS_VECTOR_SEARCH_INDEX_NAME")


def vector_db():
    vector_search_connection = MongoDBAtlasVectorSearch.from_connection_string(
        MONGO_URI,
        "document_db" + "." + "document_chunks",
        hugging_api_embeddings,
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    )

    return vector_search_connection
