from pydantic import BaseModel


class QueryModel(BaseModel):
    document_id: str
    query_text: str