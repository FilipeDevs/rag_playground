from fastapi import APIRouter
import time

from rag_v1.chains import get_retrieval_chain


rag_router_v1 = APIRouter()


@rag_router_v1.post("/chat_v1")
async def chat_v1(question: str, chat_session_id: int = 1, document: str = None):
    llm_chain = get_retrieval_chain(
        document_source=document, session_id=chat_session_id
    )

    print("Generating response...")
    start_time = time.time()
    response = llm_chain({"question": question})
    end_time = time.time()

    exec_time = round(end_time - start_time)

    print(f"Response generated in {exec_time} seconds.")
    print(f"Response : {response}")

    return {"response": response["answer"]}
