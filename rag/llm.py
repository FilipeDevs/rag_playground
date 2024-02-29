from langchain_community.llms import CTransformers
from rag.chat_history import load_chat_memory
from langchain.chains import ConversationalRetrievalChain
from rag.vector_db import vector_db

# To be revised...
config = {
    "max_new_tokens": 512,
    "temperature": 0,
    "context_length": 4096,
    "gpu_layers": 4,
}


def create_llm():
    llm = CTransformers(
        # https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/blob/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf
        model="./models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
        model_type="mistral",
        config=config,
    )

    return llm


def load_retrieval_chain(llm, vector_db, document, memory):
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_db.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5, "pre_filter": {"source": document}},
        ),
        memory=memory,
        return_source_documents=True,
    )


def setup_retrieval_chain(document_source: str, session_id: int):
    llm = create_llm()
    vector_store = vector_db()
    memory = load_chat_memory(session_id)

    llm_chain = load_retrieval_chain(
        llm=llm, vector_db=vector_store, document=document_source, memory=memory
    )

    return llm_chain
