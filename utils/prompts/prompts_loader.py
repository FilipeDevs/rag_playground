from langchain.prompts import PromptTemplate
from .prompts import STANDALONE_TEMPLATE, QUESTION_CONTEXT_TEMPLATE


def create_standalone_prompt(chat_history, question):
    return PromptTemplate.from_template(STANDALONE_TEMPLATE).format(
        chat_history=chat_history, question=question
    )


def create_question_context_prompt(context, question):
    return PromptTemplate.from_template(QUESTION_CONTEXT_TEMPLATE).format(
        context=context, question=question
    )
