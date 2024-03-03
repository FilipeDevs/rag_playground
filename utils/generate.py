import time
from llm.loader import get_llm
from utils.chats import format_chat_history, get_chat_history
from utils.prompts.prompts_loader import (
    create_question_context_prompt,
    create_standalone_prompt,
)
from utils import get_logger
from database import get_relevant_chunks


logger = get_logger()


def generate_follow_up_question(question, chat_history):
    llm = get_llm()
    standalone_prompt_formated = create_standalone_prompt(chat_history, question)
    logger.info(f"Standalone prompt formated: \n{standalone_prompt_formated}")
    response = llm(standalone_prompt_formated)

    return response


def generate_context_response(context, question):
    llm = get_llm()
    question_context_prompt_formated = create_question_context_prompt(context, question)
    logger.info(
        f"Question context prompt formated: \n{question_context_prompt_formated}"
    )
    response = llm(question_context_prompt_formated)

    return response


def generate_response(processed_question, file_ids):
    logger.info("Getting relevant chunks...")
    chunks, chunks_ids = get_relevant_chunks(
        query=processed_question, file_ids=file_ids
    )

    logger.info("Generating response...")
    start_time = time.time()
    final_response = generate_context_response(
        context=chunks, question=processed_question
    )
    end_time = time.time()
    exec_time = round(end_time - start_time)
    logger.info(f"Response generated in {exec_time} seconds")
    logger.info(f"Response: {final_response}")

    return final_response, chunks_ids


def process_chat_history(chat_id, question):
    chat_history = get_chat_history(chat_id)
    processed_question = question

    if len(chat_history) > 0:
        logger.info("Chat history found, generating follow up question...")
        formatted_chat_history = format_chat_history(chat_history)
        start_time = time.time()
        processed_question = generate_follow_up_question(
            question=question, chat_history=formatted_chat_history
        )
        end_time = time.time()
        exec_time = round(end_time - start_time)
        logger.info(
            f"Follow up question (generated in {exec_time} seconds) : {processed_question}"
        )

    return processed_question
