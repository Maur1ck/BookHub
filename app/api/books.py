from fastapi import APIRouter

from app.api.dependencies import DBDep, UserIdDep
from app.schemas.books import BookAdd, BookAddRequest
from app.services.books import BooksService

router = APIRouter(prefix="/books", tags=["Книги"])


@router.get("/")
async def get_books(db: DBDep):
    return await BooksService(db).get_books()


@router.post("/")
async def add_book(data: BookAddRequest, db: DBDep, user_id: UserIdDep):
    book = await BooksService(db).create_book(data, user_id)
    return {"status": "OK", "data": book}
