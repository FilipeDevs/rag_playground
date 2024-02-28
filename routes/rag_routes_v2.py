import time
from fastapi import APIRouter
from rag.chat_history import load_chat_memory_v2

from rag_v2.llm import get_follow_up_question, get_standalone_prompt

rag_router_v2 = APIRouter()


@rag_router_v2.post("/chatv2")
async def chat(question: str, chat_session_id: int):

    # Generate a response
    print("Generating response...")
    start_time = time.time()
    chat_history = await load_chat_memory_v2(chat_session_id).aget_messages()
    standalone_question = get_standalone_prompt()
    response = get_follow_up_question(
        standalone_question, chat_history=chat_history, question=question
    )
    end_time = time.time()
    answer = response["text"]
    exec_time = round(end_time - start_time)

    print(f"Response generated in {exec_time} seconds.")
    print(f"Standalone question : {answer}")

    return {"response": response}
