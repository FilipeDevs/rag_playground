import os
from langchain.memory import MongoDBChatMessageHistory, ConversationBufferMemory
from dotenv import load_dotenv
from database.database import db, alt_messages_collection

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")


def load_chat_memory(chat_session_id):
    message_manager = MongoDBChatMessageHistory(
        connection_string=MONGO_URI,
        session_id=chat_session_id,
        database_name=db.name,
        collection_name=alt_messages_collection.name,
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        input_key="question",
        output_key="answer",
        return_messages=True,
        chat_memory=message_manager,
    )

    return memory
