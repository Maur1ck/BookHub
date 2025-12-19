from pydantic import BaseModel


class BookAddRequest(BaseModel):
    title: str
    description: str


class BookPatch(BaseModel):
    title: str | None
    description: str | None


class BookAdd(BookAddRequest):
    author_id: int
