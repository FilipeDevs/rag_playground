from langchain_community.llms import CTransformers

# To be revised...
config = {
    "max_new_tokens": 512,
    "temperature": 0,
    "context_length": 4096,
    # Set to 0 when system has no GPU
    "gpu_layers": 5,
}


def get_llm():
    llm = CTransformers(
        # https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/blob/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf
        model="./llm/model/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
        model_type="mistral",
        config=config,
    )

    return llm
