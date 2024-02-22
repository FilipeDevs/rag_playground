import os
from fastapi import APIRouter, File, UploadFile
from database.database import file_collection
from rag.loader_splitter import load_and_split_doc
from rag.vector_db import create_vector_db, vector_db_v2
file_router = APIRouter()


@file_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Save file temporarily
    with open(file.filename, "wb") as buffer:
        buffer.write(await file.read())

    if (file.filename.endswith('.pdf') == False):
        return {"message": "Invalid file format, only PDFs are allowed"}

    if (file_collection.find_one({"source": file.filename})):
        return {"message": "File already exists"}

    # Load and split the file into chunks
    print("Loading and splitting PDF...")
    document_chunks = load_and_split_doc(file.filename)
    print(f"Number of chunks: {len(document_chunks)}")

    # Create embeddings for each chunk and store in database
    print("Storing and embedding chunks...")
    create_vector_db(document_chunks, user_id="dummy")
    # vector_db_v2(document_chunks)

    # Remove temporary file
    os.remove(file.filename)

    return {"message": "File uploaded successfully"}


@file_router.delete("/files")
async def delete_all_files():
    file_collection.delete_many({})
    return {"message": "All files deleted successfully"}


@file_router.delete("/files/{file_name}")
async def delete_file(file_name: str):
    file_collection.delete_one({"source": file_name})
    return {"message": f'{file_name} deleted successfully'}
