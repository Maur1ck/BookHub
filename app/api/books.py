from fastapi import APIRouter

from app.api.dependencies import DBDep, UserIdDep
from app.schemas.books import BookAdd, BookRequestAdd

router = APIRouter(prefix="/books", tags=["Книги"])


@router.get("/")
async def get_books(db: DBDep):
    return await db.books.get_all()


@router.post("/")
async def add_book(data: BookRequestAdd, db: DBDep, user_id: UserIdDep):
    new_data = BookAdd(**data.model_dump(), author_id=user_id)
    await db.books.add(new_data)
    await db.commit()
    return {"status": "OK"}
