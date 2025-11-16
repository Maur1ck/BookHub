from fastapi import APIRouter

from app.api.dependencies import DBDep, UserIdDep
from app.schemas.books import BookAddRequest
from app.services.books import BooksService

router = APIRouter(prefix="/books", tags=["Книги"])


@router.get("/")
async def get_books(db: DBDep):
    return await BooksService(db).get_books()


@router.get("/{book_id}")
async def get_book(book_id: int, db: DBDep):
    book = await BooksService(db).get_book(book_id)
    return {"status": "OK", "data": book}


@router.post("/")
async def add_book(data: BookAddRequest, db: DBDep, user_id: UserIdDep):
    book = await BooksService(db).create_book(data, user_id)
    return {"status": "OK", "data": book}
