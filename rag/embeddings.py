import os
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")

hugging_api_embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=api_key, 
    # Emmbbeddings Leaderboard: https://huggingface.co/spaces/mteb/leaderboard
    # This one makes 384 dimension embeddings, maybe we could use something bigger ?
    # Atlas Vector Search Index is set to 384, so if the embeddings are bigger/smaller, we need to change it
    model_name="sentence-transformers/all-MiniLM-l6-v2"
)