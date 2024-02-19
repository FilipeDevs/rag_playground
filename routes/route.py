import os
from fastapi import APIRouter, File, UploadFile
from config.database import file_collection
from rag.manual_embedding import manual_create_embeddings
from rag.vector_search import generate_embedding_mongo_atlas
from rag.doc_loader_splitter import load_and_split_pdf
from rag.vector_query import vector_search_connection
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFaceHub
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Save file temporarily
    with open(file.filename, "wb") as buffer:
        buffer.write(await file.read())

    if(file.filename.endswith('.pdf') == False):
        return {"message": "Invalid file format"}

    if(file_collection.find_one({"source": file.filename})):
        return {"message": "File already exists"}

    # Load and split the file into chunks
    print("Loading and splitting PDF...")
    document_chunks = load_and_split_pdf(file.filename)

    # Create embeddings for each chunk and store in database
    manual_create_embeddings(document_chunks, file, user_id="user_id")

    # The documents generated from this library unfortunately don't allow to add additional fields to the documents, like user_id
    # generate_embedding_mongo_atlas(document_chunks)
    
    # Remove temporary file
    os.remove(file.filename)

    return {"message": "File uploaded successfully"}




@router.post("/question-answer")
async def query_document(query: str):
    # Generate embedding for the query

    qa_retriever = vector_search_connection.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 10},
    )

    prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    Question: {question}
    """
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    qa = RetrievalQA.from_chain_type(
        llm= HuggingFaceHub(
            repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
        ),
        chain_type="stuff",
        retriever=qa_retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT},
    )

    docs = qa({"query": query})

    print(docs["result"])
    # print(docs["source_documents"])

    return {"result": docs["result"]}
    


@router.delete("/delete")
async def delete_file(file: str):
    file_collection.delete_many({"source": file})
    return {"message": "File deleted successfully"}

