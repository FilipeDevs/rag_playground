import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongo_url = os.getenv("MONGO_URI")

client = MongoClient(mongo_url)

db = client.document_db

file_collection = db["document_chunks"]