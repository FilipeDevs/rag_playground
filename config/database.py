from pymongo import MongoClient

MONGO_URI = "mongodb+srv://admin:FNbrux12ISU@cluster0.dzb7poz.mongodb.net/?retryWrites=true&w=majority"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "semantic_search_pdf"

client = MongoClient(MONGO_URI)

db = client.document_db

file_collection = db["document_chunks"]

