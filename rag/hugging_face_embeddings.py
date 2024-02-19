from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings

HUGGING_FACE_API_KEY = "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"

hugging_api_embeddings = HuggingFaceInferenceAPIEmbeddings(
    api_key=HUGGING_FACE_API_KEY, model_name="sentence-transformers/all-MiniLM-l6-v2"
)