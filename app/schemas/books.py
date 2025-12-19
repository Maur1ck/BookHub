from pydantic import BaseModel


class BookAddRequest(BaseModel):
    title: str
    description: str


class BookPatch(BaseModel):
    title: str | None = None
    description: str | None = None


class BookAdd(BookAddRequest):
    author_id: int
