from fastapi import FastAPI
from routes.rag_routes_v1 import rag_router_v1
from routes.file_routes import file_router
from routes.rag_routes_v2 import rag_router_v2
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(file_router)
app.include_router(rag_router_v1)
app.include_router(rag_router_v2)
