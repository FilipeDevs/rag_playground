from rag.hugging_face_embeddings import hugging_api_embeddings
from config.database import file_collection


def manual_create_embeddings(document_chunks, file, user_id):
     for chunk_id, chunk_text in enumerate(document_chunks):
       emebedding = hugging_api_embeddings.embed_query(chunk_text.page_content)
       chunk_data = {
           "source": file.filename,
           "chunk_id": chunk_id,
           "text": chunk_text.page_content,
           "embedding": emebedding,
           "user_id": user_id,
       }

       file_collection.insert_one(chunk_data)
        