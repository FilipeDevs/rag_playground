from utils.rag_v1.chats_memory import load_chat_memory
from langchain.chains import ConversationalRetrievalChain
from database import get_vector_db
from llm.loader import get_llm


def load_retrieval_chain(llm, vector_db, file_id, memory):
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_db.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5, "pre_filter": {"source": file_id}},
        ),
        memory=memory,
        return_source_documents=True,
        verbose=True,
    )


def get_retrieval_chain(file_id: str, session_id: int):
    llm = get_llm()
    vector_store = get_vector_db()
    memory = load_chat_memory(session_id)

    llm_chain = load_retrieval_chain(
        llm=llm, vector_db=vector_store, file_id=file_id, memory=memory
    )

    return llm_chain
