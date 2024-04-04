from langchain.prompts import PromptTemplate
from .prompts import STANDALONE_TEMPLATE, QUESTION_CONTEXT_TEMPLATE
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema import SystemMessage


def create_standalone_prompt(chat_history, question):
    return ChatPromptTemplate.from_template(STANDALONE_TEMPLATE).format(
        chat_history=chat_history, question=question
    )


def create_question_context_prompt(context, question):
    return ChatPromptTemplate.from_template(QUESTION_CONTEXT_TEMPLATE).format(
        context=context, question=question
    )


def create_question_context_prompt_v2(context):
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=f"""Use the following pieces of context to answer the human input at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. qIf the question is not relevant to the context, just say that 'I don't know'.
                Context: 
                {context}
                """
            ),
            HumanMessagePromptTemplate.from_template("{human_input}"),
        ]
    )

    return prompt


def create_standalone_prompt_v2(chat_history):
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=f"""Use the following chat history to answer the human input at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. If the question is not relevant to the context, just say that 'I don't know'.
                Chat history: 
                {chat_history}
                """
            ),
            HumanMessagePromptTemplate.from_template("{human_input}"),
        ]
    )

    return prompt
