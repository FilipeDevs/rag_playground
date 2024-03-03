from fastapi import APIRouter
import time
from utils import get_logger
from utils.rag_v1.chains import get_retrieval_chain

logger = get_logger()
rag_router_v1 = APIRouter()


@rag_router_v1.post("/chat_v1")
async def chat_v1(question: str, chat_session_id: int = 1, file_id: str = None):
    llm_chain = get_retrieval_chain(file_id=file_id, session_id=chat_session_id)

    start_time = time.time()

    logger.info(f'Generating response for question : "{question}"')
    response = llm_chain({"question": question})

    end_time = time.time()
    exec_time = round(end_time - start_time)

    logger.info(f"Response generated in {exec_time} seconds.")
    logger.info(f"Response : {response}")

    return {"response": response["answer"]}
