from fastapi import APIRouter
from bson import ObjectId
from utils import get_chat_files
from utils import (
    generate_response,
    add_message_to_chat,
)
from database import chats_collection
from utils import get_logger

from utils.generate import process_chat_history

rag_router_v2 = APIRouter()

logger = get_logger()


@rag_router_v2.post("/chat_v2")
async def chat_v2(question: str, chat_id: str):
    processed_question = question.strip()

    if chats_collection.find_one({"_id": ObjectId(chat_id)}) is None:
        logger.warning(f"No chat found with id: {chat_id}")
        return {"response": f"No chat found with id: {chat_id}"}

    processed_question = process_chat_history(chat_id, processed_question)

    file_ids = get_chat_files(chat_id)
    final_response, chunks_ids = generate_response(
        processed_question=processed_question, file_ids=file_ids
    )

    add_message_to_chat(chat_id, text=question, type="Human")
    add_message_to_chat(
        chat_id, text=final_response.strip(), type="Assistant", chunks_ids=chunks_ids
    )

    return {"response": {final_response}}
