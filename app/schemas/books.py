from pydantic import BaseModel


class BookAddRequest(BaseModel):
    title: str
    description: str


class BookAdd(BookAddRequest):
    author_id: int
