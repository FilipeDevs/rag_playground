from llm.loader import get_llm
from utils.prompts.prompts_loader import (
    create_question_context_prompt,
    create_standalone_prompt,
)


def generate_follow_up_question(question, chat_history):
    llm = get_llm()
    standalone_prompt_formated = create_standalone_prompt(chat_history, question)
    print(standalone_prompt_formated)
    response = llm(standalone_prompt_formated)

    return response


def generate_context_response(context, question):
    llm = get_llm()
    question_context_prompt_formated = create_question_context_prompt(context, question)
    print(question_context_prompt_formated)
    response = llm(question_context_prompt_formated)

    return response
