import requests
import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = pymongo.MongoClient(MONGO_URI)
db = client.sample_mflix
collection = db.movies

hugging_face_api_key = os.getenv("HUGGING_FACE_API_KEY")
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

def generate_embedding(text : str) -> list[float]:
    """
    Generate an embedding for a given text using the Hugging Face API. 
    An embedding is a numerical representation of the text that can be used for similarity comparisons.
    Lets say we have a text "I am happy" and "I am sad", the embeddings for these two texts will be similar.
    An embedding is essentially a list(vector) of numbers that represents the text.
    """
    response = requests.post(
        embedding_url,
        headers={"Authorization": f"Bearer {hugging_face_api_key}"},
        json={"inputs": text})
    
    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code}")
    
    return response.json()


# Add a new field to 50 documents in the collection with the plot embedding
for doc in collection.find({'plot': {'$exists': True}}).limit(50):
   # Generate the embedding for the plot and add it to the document
   doc['plot_embedding_hf'] = generate_embedding(doc['plot'])
   collection.replace_one({'_id': doc['_id']}, doc)