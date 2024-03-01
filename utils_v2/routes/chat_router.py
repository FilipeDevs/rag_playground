import time
from fastapi import APIRouter
from models import Chat, Message
from datetime import datetime
from utils.chat_history import load_chat_memory
from utils.llm import (
    generate_follow_up_question,
    get_relevant_docs,
    generate_context_response,
)
from utils.chat_history_v2 import (
    create_new_chat,
    get_chat_history,
    add_message_to_chat,
    format_chat_history,
)

chat_router = APIRouter()


@chat_router.post("/create_chat")
async def create_chat(chat: Chat):
    chat_id = create_new_chat(chat)

    return {"response": f"Chat created successfully with id {chat_id}"}


@chat_router.get("/chat_history")
async def get_chat_history_(chat_id: str):
    chat_history = get_chat_history(chat_id)

    return {"response": f"Chat history {chat_history}"}


@chat_router.post("/add_message")
async def add_message_(chat_id: str, message: str, type: str):
    message = Message(message=message, type=type, date=datetime.now())
    add_message_to_chat(chat_id, message)
    return {"response": f"Message added to chat successfully."}


@chat_router.post("/chat")
async def chat(question: str, chat_session_id: str):

    print("Generating standalone question...")
    chat_history = get_chat_history(chat_session_id)
    print(format_chat_history(chat_history))
    # start_time = time.time()
    # chat_history = await load_chat_memory(chat_session_id).aget_messages()
    # response = generate_follow_up_question(chat_history=chat_history, question=question)
    # standalone_question = response
    # end_time = time.time()
    # exec_time = round(end_time - start_time)

    # print(f"Question generated in {exec_time} seconds.")
    # print(f"Standalone question : {standalone_question}")

    # docs = get_relevant_docs(question=standalone_question)
    # print(f"Relevant docs: {docs}")

    # print("Generating final answer...")
    # start_time = time.time()
    # final_response = generate_context_response(
    #     context=docs, question=standalone_question
    # )
    # end_time = time.time()
    # exec_time = round(end_time - start_time)
    # print(f"Answer generated in {exec_time} seconds.")
    # print(f"Final answer: {final_response}")

    # # print(final_response)

    return {"response": "OK"}
