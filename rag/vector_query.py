from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from rag.hugging_face_embeddings import hugging_api_embeddings
from config.database import ATLAS_VECTOR_SEARCH_INDEX_NAME
from config.database import MONGO_URI

vector_search_connection = MongoDBAtlasVectorSearch.from_connection_string(
    MONGO_URI,
    "document_db" + "." + "document_chunks",
    hugging_api_embeddings,
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
)