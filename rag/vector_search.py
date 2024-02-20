from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from rag.hugging_face_embeddings import hugging_api_embeddings
from config.database import file_collection
from config.database import ATLAS_VECTOR_SEARCH_INDEX_NAME


def generate_embedding_mongo_atlas(docs):
    vector_store = MongoDBAtlasVectorSearch.from_documents(
        documents=docs,
        embedding=hugging_api_embeddings,
        collection=file_collection,
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    )

    return vector_store
