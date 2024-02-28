from langchain_community.llms import CTransformers
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from rag_v2.prompts import standalone_prompt

# To be revised...
config = {
    "max_new_tokens": 512,
    "temperature": 0,
    "context_length": 4096,
    "gpu_layers": 4,
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


def get_follow_up_question(prompt, question, chat_history):
    llm = get_llm()
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    response = llm_chain.invoke({"chat_history": chat_history, "question": question})

    return response
