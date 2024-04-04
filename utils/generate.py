import time
from llm.loader import get_azure_llm
from utils.chats import format_chat_history, get_chat_history
from utils.prompts.prompts_loader import (
    create_question_context_prompt_v2,
    create_standalone_prompt_v2,
)
from langchain.chains import LLMChain
from utils.logger import get_logger
from utils.retrievers import get_relevant_context

logger = get_logger()


def generate_follow_up_question(question, chat_history):
    llm = get_azure_llm()
    prompt = create_standalone_prompt_v2(chat_history, question)
    chat_llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True,
    )

    result = chat_llm_chain.predict(human_input=question)
    logger.info(f"Response: {result}")

    return result


def generate_context_response(context, question):
    llm = get_azure_llm()
    prompt = create_question_context_prompt_v2(context)
    chat_llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True,
    )
    result = chat_llm_chain.predict(human_input=question)
    logger.info(f"Response: {result}")

    return result


def generate_response(processed_question, file_ids):

    logger.info("Getting relevant chunks...")

    context_text, chunks_ids = get_relevant_context(processed_question, file_ids)

    logger.info("Generating response...")

    start_time = time.time()
    final_response = generate_context_response(
        context=context_text, question=processed_question
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
