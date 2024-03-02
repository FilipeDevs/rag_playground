import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongo_url = os.getenv("MONGO_URI")

client = MongoClient(mongo_url)

db = client.rag

chunks_collection = db["chunks"]
chats_collection = db["chats"]
messages_collection = db["messages"]
alt_messages_collection = db["messages_alt"]
files_collection = db["files"]
