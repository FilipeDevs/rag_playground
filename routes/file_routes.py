import os
from fastapi import APIRouter, File, UploadFile
from utils.loader_splitter import load_and_split_doc
from utils.signature import generate_file_signature
from database import insert_chunks_to_vector_db
from database import files_collection, chunks_collection
from models import FileUpload
from datetime import datetime
from bson import ObjectId

file_router = APIRouter()


@file_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Save file temporarily
    with open(file.filename, "wb") as buffer:
        buffer.write(await file.read())

    if file.filename.endswith(".pdf") == False:
        os.remove(file.filename)
        return {"message": "Invalid file format, only PDFs are allowed"}

    # Generate SHA256 hash as the signature
    signature = generate_file_signature(file.filename)

    # Check if a file with the same signature exists
    existing_file = files_collection.find_one({"signature": signature})
    if existing_file:
        # If the file contents already exist, the new file will point to the original file
        print(
            f"File contents already exist, {file.filename} file will point to original file."
        )
        os.remove(file.filename)
        original_file_id = str(existing_file["_id"])
        new_file = FileUpload(
            name=file.filename,
            uploaded_at=datetime.now(),
            original_file_id=original_file_id,
            is_original=False,
        )
        files_collection.insert_one(dict(new_file))
    else:
        # If the file contents do not exist, the new file will be stored and marked as original
        print(
            f"First time file contents, {file.filename} will be stored as an original file."
        )
        new_file = FileUpload(
            name=file.filename,
            uploaded_at=datetime.now(),
            signature=signature,
            is_original=True,
        )
        file_id = files_collection.insert_one(dict(new_file)).inserted_id
        # Load and split the file into chunks
        print("Loading and splitting PDF file...")
        document_chunks = load_and_split_doc(file.filename)
        print(f"Number of chunks created: {len(document_chunks)}")

        # Create embeddings for each chunk and store in database
        print("Storing and embedding chunks...")
        # Chunks will point to the file that contains them
        insert_chunks_to_vector_db(document_chunks, file_id)
        # Remove temporary file
        os.remove(file.filename)

    print(f"File {file.filename} uploaded successfully")
    return {"message": f"File {file.filename} uploaded successfully"}


@file_router.delete("/files/{file_id}")
async def delete_file(file_id: str):
    result = chunks_collection.delete_many({"source": file_id}).deleted_count

    if result == 0:
        return {"message": f"File {file_id} does not exist"}

    files_collection.find_one_and_delete({"_id": ObjectId(file_id)})

    return {"message": f"{file_id} deleted successfully"}
