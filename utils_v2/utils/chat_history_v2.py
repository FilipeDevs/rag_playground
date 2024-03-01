from datetime import datetime

from bson import ObjectId
from db.config import chat_collection, messages_collection
from models import Message, Chat


def create_new_chat(chat: Chat):
    chat_id = chat_collection.insert_one(dict(chat)).inserted_id

    return chat_id


def create_new_message(message: Message):
    return messages_collection.insert_one(dict(message)).inserted_id


def add_message_to_chat(chat_id, message: Message):
    message_id = create_new_message(message)
    chat_collection.find_one_and_update(
        {"_id": ObjectId(chat_id)}, {"$push": {"messages": message_id}}
    )


def get_chat_history(chat_id, limit=10):
    chat = chat_collection.find_one({"_id": ObjectId(chat_id)})
    messages = (
        messages_collection.find({"_id": {"$in": chat["messages"]}})
        .sort([("date", 1)])
        .limit(limit)
    )

    return list(messages)


def format_chat_history(messages):
    formatted_history = ""
    for message in messages:
        if message["type"] == "AI":
            formatted_history += "AI: " + message["message"] + "\n"
        elif message["type"] == "Human":
            formatted_history += "Human: " + message["message"] + "\n"
    return formatted_history.strip()


def get_chat_files(chat_id):
    """
    Get files from chat, using a projection to only return the files field (and exclude the _id field).
    """
    return chat_collection.find_one({"_id": ObjectId(chat_id)}, {"files": 1, "_id": 0})[
        "files"
    ]
