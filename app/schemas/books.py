from pydantic import BaseModel


class BookRequestAdd(BaseModel):
    title: str
    description: str


class BookAdd(BookRequestAdd):
    author_id: int
