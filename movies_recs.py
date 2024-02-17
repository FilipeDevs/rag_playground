from generate_embedding import generate_embedding
import pymongo
import os
from dotenv import load_dotenv



load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = pymongo.MongoClient(MONGO_URI)
db = client.sample_mflix
collection = db.movies

hugging_face_api_key = os.getenv("HUGGING_FACE_API_KEY")
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"


query = "Imaginary characters from outer space at war"


# Use the $vectorSearch aggregation stage to find the most similar documents to the query
# MongoDB will use the plot_embedding_hf field to find the most similar documents based on the embedding of the query
# The numCandidates parameter specifies the number of documents to consider for the search
# The limit parameter specifies the number of documents to return
# The index parameter specifies the name of the index to use for the search (created in MongoDB Atlas Search)
results = collection.aggregate([
    {"$vectorSearch": {
        "queryVector" : generate_embedding(query),
        "path": "plot_embedding_hf",
        "numCandidates" : 100,
        "limit" : 4,
        "index" : "plot_semantic_search",
    }}
])

for document in results:
    print(f'Movie Name: {document["title"]}, \nMovie Plot: {document["plot"]}\n')

