from pydantic import BaseModel


class Chat(BaseModel):
    name: str
    messages: list[str] = []
    files: list[str]
