from bson import ObjectId
from langchain_community.llms import CTransformers
from langchain.prompts import PromptTemplate
from utils.prompts import STANDALONE_TEMPLATE, QUESTION_CONTEXT_TEMPLATE

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
        model="./llm_models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
        model_type="mistral",
        config=config,
    )

    return llm


def get_standalone_prompt(chat_history, question):
    return PromptTemplate.from_template(STANDALONE_TEMPLATE).format(
        chat_history=chat_history, question=question
    )


def get_question_context_prompt(context, question):
    return PromptTemplate.from_template(QUESTION_CONTEXT_TEMPLATE).format(
        context=context, question=question
    )


def get_relevant_docs(question: str, chunk_ids: list[str]):
    # Convert chunk_ids to ObjectId if necessary
    chunk_object_ids = [chunk_id for chunk_id in chunk_ids]
    results = vector_db().similarity_search_with_score(
        query=question, k=5, pre_filter={"_id": {"$in": chunk_ids}}
    )

    if len(results) == 0 or results[0][1] < 0.75:
        print(f"Unable to find matching results.")
        return

    return format_relevant_docs(results)


def format_relevant_docs(docs):
    context_text = "\n\n".join([doc.page_content for doc, _score in docs])

    return context_text


def generate_follow_up_question(question, chat_history):
    llm = get_llm()
    standalone_prompt_formated = get_standalone_prompt(chat_history, question)
    print(standalone_prompt_formated)
    response = llm(standalone_prompt_formated)

    return response


def generate_context_response(context, question):
    llm = get_llm()
    question_context_prompt_formated = get_question_context_prompt(context, question)
    print(question_context_prompt_formated)
    response = llm(question_context_prompt_formated)

    return response
