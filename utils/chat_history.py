import os
from langchain.memory import MongoDBChatMessageHistory
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")


def load_chat_memory(chat_session_id) -> MongoDBChatMessageHistory:
    message_manager = MongoDBChatMessageHistory(
        connection_string=MONGO_URI,
        session_id=chat_session_id,
        database_name="chat_history",
        collection_name="messages",
    )

    return message_manager
