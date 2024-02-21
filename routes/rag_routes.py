from fastapi import APIRouter
import time
from rag.llm import setup_retrieval_chain

rag_router = APIRouter()

@rag_router.post("/chat")
async def chat(question : str, chat_session_id : int = 1, document : str = "Counter-Strike.pdf"):
    
    # Load the retrieval chain
    llm_chain = setup_retrieval_chain(document_source=document, session_id=chat_session_id)
    
    # Generate a response
    print("Generating response...")
    start_time = time.time()
    response = llm_chain({'question': question})
    end_time = time.time()
    
    exec_time = end_time - start_time
    print(f"Response generated in {exec_time} seconds.")
    print(f"Response : {response}")

    return {"response": response["answer"]}
