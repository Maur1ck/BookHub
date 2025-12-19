from fastapi import APIRouter

from app.api.dependencies import DBDep, UserIdDep, AuthorOrAdminDep
from app.schemas.books import BookAddRequest
from app.services.books import BooksService
from app.schemas.books import BookPatch

router = APIRouter(prefix="/books", tags=["Книги"])


# добавить некую фильтрацию
@router.get("/", summary="Публичный список книг")
async def get_books(db: DBDep):
    return await BooksService(db).get_books()


@router.get("/my", summary="Книги текущего автора")
async def get_my_books(db: DBDep, current_user: AuthorOrAdminDep):
    return await BooksService(db).get_books_by_author(current_user.id)


@router.get("/{book_id}")
async def get_book(book_id: int, db: DBDep):
    book = await BooksService(db).get_book(book_id)
    return {"status": "OK", "data": book}


@router.post("/")
async def add_book(data: BookAddRequest, db: DBDep, current_user: AuthorOrAdminDep):
    book = await BooksService(db).create_book(data, current_user.id)
    return {"status": "OK", "data": book}


@router.put("/{book_id}")
async def update_book(
        book_id: int,
        data: BookAddRequest,
        db: DBDep,
        current_user: AuthorOrAdminDep
):
    await BooksService(db).edit_book(book_id, data, current_user.id)
    return {"status": "OK"}


@router.patch("/{book_id}")
async def update_book_partially(
        book_id: int,
        data: BookPatch,
        db: DBDep,
        current_user: AuthorOrAdminDep
):
    await BooksService(db).edit_book_partially(book_id, data, current_user.id)
    return {"status": "OK"}


@router.delete("/{book_id}")
async def delete_book(book_id: int, db: DBDep, user_id: UserIdDep):
    ...
