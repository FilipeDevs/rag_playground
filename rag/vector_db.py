import os
from database.database import file_collection
from rag.embeddings import hugging_api_embeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
ATLAS_VECTOR_SEARCH_INDEX_NAME = os.getenv("ATLAS_VECTOR_SEARCH_INDEX_NAME")

def create_vector_db(document_chunks, file, user_id):
    for chunk_id, chunk_text in enumerate(document_chunks):
        emebedding = hugging_api_embeddings.embed_query(chunk_text.page_content)
        chunk_data = {
           "source": file.filename,
           "chunk_id": chunk_id,
           "text": chunk_text.page_content,
           "embedding": emebedding,
           "user_id": user_id, # Who the document belongs to
        }

        file_collection.insert_one(chunk_data)
        
def vector_db():
    vector_search_connection = MongoDBAtlasVectorSearch.from_connection_string(
        MONGO_URI,
        "document_db" + "." + "document_chunks",
        hugging_api_embeddings,
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    )

    return vector_search_connection
