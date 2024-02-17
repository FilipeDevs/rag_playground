import pymongo
import os
from dotenv import load_dotenv
import requests


load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = pymongo.MongoClient(MONGO_URI)
db = client.sample_mflix
collection = db.movies

hugging_face_api_key = os.getenv("HUGGING_FACE_API_KEY")
embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

def generate_embedding(text : str) -> list[float]:

    response = requests.post(
        embedding_url,
        headers={"Authorization": f"Bearer {hugging_face_api_key}"},
        json={"inputs": text})
    
    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code}")
    
    return response.json()


print(generate_embedding("freeCodeCamp is awesome"))


