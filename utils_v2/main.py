from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import chat_router, rag_router
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=chat_router)
app.include_router(router=rag_router)
