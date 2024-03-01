import os
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")

hugging_api_embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=api_key,
    model_name="sentence-transformers/all-MiniLM-l6-v2",
)
