from langchain_community.llms import CTransformers
from langchain.prompts import PromptTemplate
from utils.prompts import standalone_prompt, question_context_prompt
from langchain.chains import LLMChain

from utils.vector_db import vector_db

# To be revised...
config = {
    "max_new_tokens": 512,
    "temperature": 0,
    "context_length": 4096,
    "gpu_layers": 0,
}


def get_llm():
    llm = CTransformers(
        # https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/blob/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf
        model="./models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
        model_type="mistral",
        config=config,
    )

    return llm


def get_standalone_prompt():
    _template = standalone_prompt

    STANDALONE_QUESTION_PROMPT = PromptTemplate(
        template=_template,
        input_variables=["chat_history", "question"],
    )

    return STANDALONE_QUESTION_PROMPT


def get_question_context_prompt():
    _template = question_context_prompt

    QUESTION_CONTEXT_PROMPT = PromptTemplate(
        template=_template,
        input_variables=["context", "question"],
    )

    return QUESTION_CONTEXT_PROMPT


def generate_follow_up_question(prompt, question, chat_history):
    llm = get_llm()
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    response = llm_chain.invoke({"chat_history": chat_history, "question": question})

    return response


def get_relevant_docs(question: str):
    results = vector_db().similarity_search(query=question, k=3)

    return format_relevant_docs(results)


def format_relevant_docs(docs):
    formatted_docs = ""

    # Display results
    for doc in docs:
        formatted_doc = doc.page_content.replace(
            "\n", " "
        )  # Replace newlines with spaces
        formatted_docs += formatted_doc + "\n\n"

    return formatted_docs


def generate_context_response(context, question):
    llm = get_llm()
    llm_chain = LLMChain(llm=llm, prompt=get_question_context_prompt())
    response = llm_chain.invoke({"context": context, "question": question})

    return response
