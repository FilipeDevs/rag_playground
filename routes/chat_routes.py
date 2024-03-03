from fastapi import APIRouter
from models import Chat
from bson import ObjectId
from database import chats_collection, files_collection
from utils import get_logger

chat_router = APIRouter()

logger = get_logger()


@chat_router.post("/create_chat")
async def create_chat(chat: Chat):
    # Check if all files exist
    for file_id in chat.files:
        file = files_collection.find_one({"_id": ObjectId(file_id)})
        if file is None:
            logger.warning(
                f"File with id {file_id} not found, chat will not be created"
            )
            return {
                "error": f"File with id {file_id} not found, chat can not be created"
            }

    chat_id = chats_collection.insert_one(dict(chat)).inserted_id
    logger.info(f"Chat with id {chat_id} created")
    return {"chat_id": str(chat_id)}


@chat_router.post("/add_file_to_chat")
async def add_file_to_chat(chat_id: str, file_id: str):
    chat = chats_collection.find_one({"_id": ObjectId(chat_id)})
    if chat is None:
        logger.warning(f"Chat with id {chat_id} not found")
        return {"error": f"Chat with id {chat_id} not found"}

    file = files_collection.find_one({"_id": ObjectId(file_id)})
    if file is None:
        logger.warning(f"File with id {file_id} not found")
        return {"error": f"File with id {file_id} not found"}

    chats_collection.update_one(
        {"_id": ObjectId(chat_id)}, {"$push": {"files": file_id}}
    )
    logger.info(f"File with id {file_id} added to chat with id {chat_id}")
    return {"chat_id": chat_id, "file_id": file_id}
