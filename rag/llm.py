from langchain_community.llms import CTransformers
from rag.chat_history import load_chat_memory
from langchain.chains import ConversationalRetrievalChain, StuffDocumentsChain
from rag.vector_db import vector_db
from langchain_core.prompts import PromptTemplate
# To be revised...
config = {'max_new_tokens': 512, 'temperature' : 0, 'context_length': 4096, 'gpu_layers' : 0}

def create_llm():
    llm = CTransformers(
        # Seemed a good model for testing, not too slow not too dumb
        # https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/blob/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf
        model="./models/mistral-7b-instruct-v0.1.Q4_K_M.gguf", 
        model_type="mistral",
        config=config
    )

    return llm


def load_conversational_chain(llm, vector_db, document, memory):
    document_prompt = PromptTemplate(
        input_variables=["page_content"],
        template="{page_content}"
    )

    document_variable_name = "context"
    llm=create_llm()

    

def load_retrieval_chain(llm, vector_db, document, memory):
    # This chain works really well for retrieval because it uses the LLM to generate a prompt to make standalone queries
    # based of chat history. The issue is that it's performance is not as good as the other chains because for a single
    # query it has to prompt the LLM at least twice. Once to generate the prompt(standalone query) and once to generate the response.
    return ConversationalRetrievalChain.from_llm(llm=llm, 
                                                retriever=vector_db.as_retriever(
                                                    search_type="similarity",
                                                    search_kwargs={"k": 5, "pre_filter" : {"source": document}}
                                                ), 
                                                memory=memory,
)


def setup_retrieval_chain(document_source : str, session_id : int):
    llm = create_llm()
    vector_store = vector_db()
    memory = load_chat_memory(session_id)

    llm_chain = load_retrieval_chain(llm=llm, vector_db=vector_store, document=document_source, memory=memory)

    return llm_chain