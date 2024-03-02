from bson import ObjectId
from database import files_collection


def get_chunks_from_file(file_id: str):
    chunks = files_collection.find({"_id": ObjectId(file_id)})["chunks_ids"]
    return chunks


def get_chunks_from_files(file_ids: list[str]):
    chunks = []
    for file_id in file_ids:
        chunks += get_chunks_from_file(file_id)
    return chunks
