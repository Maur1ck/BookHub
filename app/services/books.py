from fastapi import HTTPException

from app.exceptions import ObjectNotFoundException
from app.schemas.books import BookAddRequest, BookAdd
from app.services.base import BaseService


class BooksService(BaseService):
    async def get_books(self):
        return await self.db.books.get_all()

    async def get_book(self, book_id: int):
        try:
            return await self.db.books.get_one(id=book_id)
        except ObjectNotFoundException:
            raise HTTPException(status_code=404, detail="Книга не найдена")

    async def create_book(self, data: BookAddRequest, user_id: int):
        new_data = BookAdd(**data.model_dump(), author_id=user_id)
        book = await self.db.books.add(new_data)
        await self.db.commit()
        return book
