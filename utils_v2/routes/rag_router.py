import time
from fastapi import APIRouter
from utils.chat_history_v2 import get_chat_files, get_chat_history, format_chat_history
from utils.llm import (
    generate_context_response,
    generate_follow_up_question,
    get_relevant_docs,
)
from colorama import Fore


rag_router = APIRouter()


@rag_router.post("/qa")
async def qa(question: str, chat_id: str = None, source: str = "Belgium_Wiki.pdf"):
    final_question = question
    # chat_history = get_chat_history(chat_id)
    # associated_docs = get_chat_files(chat_id)
    # print(associated_docs)
    # print(Fore.GREEN + "Generating standalone question..." + Fore.RESET)
    # start_time = time.time()
    # response = generate_follow_up_question(
    #     chat_history=format_chat_history(chat_history), question=question
    # )
    # final_question = response
    # end_time = time.time()
    # exec_time = round(end_time - start_time)

    # print(f"Standalone question (generated in {exec_time} seconds) : {final_question}")

    # print("Retrieving relevant documents...")
    docs = get_relevant_docs(
        question=final_question,
        chunk_ids=[
            "65e19a074afe1d3ca531c7db",
            "65e19a074afe1d3ca531c7da",
            "65e19a084afe1d3ca531c7dc",
        ],
    )

    # print("Generating final answer...")
    # start_time = time.time()
    # final_response = generate_context_response(context=docs, question=final_question)
    # end_time = time.time()
    # exec_time = round(end_time - start_time)
    # print(f"Final answer (generated in {exec_time} seconds) : {final_response}")

    return {"response": "OK"}
