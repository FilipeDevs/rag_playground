from langchain_community.llms import CTransformers
from langchain_mistralai.chat_models import ChatMistralAI
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv


load_dotenv()
# To be revised...
config = {
    "max_new_tokens": 512,
    "temperature": 0.4,
    "context_length": 4096,
    # Set to 0 when system has no GPU
    "gpu_layers": 0,
}


def get_llm():
    llm = CTransformers(
        # https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/blob/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf
        model="./llm/model/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
        model_type="mistral",
        config=config,
    )

    return llm


def get_azure_llm():
    llm = ChatMistralAI(
        name="Mistral-large-cody",
        endpoint=os.getenv("MISTRAL_ENDPOINT"),
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
    )

    return llm
