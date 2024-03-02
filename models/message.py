from pydantic import BaseModel
from datetime import datetime


class Message(BaseModel):
    type: str
    text: str
    date: datetime
    chunks_ids: list[str] = []
