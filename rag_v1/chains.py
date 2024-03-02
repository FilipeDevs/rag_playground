from rag_v1.chats import load_chat_memory
from langchain.chains import ConversationalRetrievalChain
from database import vector_db
from llm.loader import get_llm


def load_retrieval_chain(llm, vector_db, document, memory):
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_db.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5, "pre_filter": {"source": document}},
        ),
        memory=memory,
        return_source_documents=True,
        verbose=True,
    )


def get_retrieval_chain(document_source: str, session_id: int):
    llm = get_llm()
    vector_store = vector_db()
    memory = load_chat_memory(session_id)

    llm_chain = load_retrieval_chain(
        llm=llm, vector_db=vector_store, document=document_source, memory=memory
    )

    return llm_chain
