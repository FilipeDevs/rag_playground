from pydantic import BaseModel


class Chunk(BaseModel):
    source: str
    page_number: int
    text: str
    embedding: list[float]
