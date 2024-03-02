import time
from fastapi import APIRouter
from database.vector_db import get_relevant_docs
from rag_v2.chats import get_chat_history, get_chat_files
from utils.chunks import get_chunks_from_files
from rag_v2 import generate_context_response, generate_follow_up_question

rag_router_v2 = APIRouter()


@rag_router_v2.post("/chat_v2")
async def chat_v2(question: str, chat_id: str = None):
    chat_history = get_chat_history(chat_id)
    files_ids = get_chat_files(chat_id)
    chunk_ids = get_chunks_from_files(files_ids)
    start_time = time.time()
    standalone_question = generate_follow_up_question(
        question=question, chat_history=chat_history
    )
    end_time = time.time()
    exec_time = round(end_time - start_time)

    print(
        f"Standalone question (generated in {exec_time} seconds) : {standalone_question}"
    )

    print("Retrieving relevant documents...")
    docs = get_relevant_docs(question=standalone_question, chunk_ids=chunk_ids)

    print("Generating final answer...")
    start_time = time.time()
    final_response = generate_context_response(
        context=docs, question=standalone_question
    )
    end_time = time.time()
    exec_time = round(end_time - start_time)
    print(f"Final answer (generated in {exec_time} seconds) : {final_response}")

    return {"response": "OK"}
