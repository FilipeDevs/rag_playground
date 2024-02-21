import os
from langchain.memory import MongoDBChatMessageHistory, ConversationBufferMemory
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

def load_chat_memory(chat_session_id):
    message_manager = MongoDBChatMessageHistory(
        connection_string=MONGO_URI,
        session_id=chat_session_id,  
        database_name="chat_history",
        collection_name="messages"
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        chat_memory=message_manager,
    )

    return memory