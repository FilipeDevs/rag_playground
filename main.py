from fastapi import FastAPI
from routes.rag_routes import rag_router
from routes.file_routes import file_router
from routes.rag_routes_v2 import rag_router_v2
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(rag_router)
app.include_router(file_router)
app.include_router(rag_router_v2)
