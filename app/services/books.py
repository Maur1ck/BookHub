from fastapi import HTTPException

from app.core.exceptions import ObjectNotFoundException, ObjectNotFoundHTTPException
from app.schemas.books import BookAddRequest, BookAdd
from app.services.base import BaseService
from app.schemas.books import BookPatch


class BooksService(BaseService):
    async def get_books(self):
        return await self.db.books.get_all()

    async def get_book(self, book_id: int):
        try:
            return await self.db.books.get_one(id=book_id)
        except ObjectNotFoundException:
            raise ObjectNotFoundHTTPException

    async def get_books_by_author(self, user_id: int):
        return await self.db.books.get_filtered(author_id=user_id)

    async def create_book(self, data: BookAddRequest, user_id: int):
        new_data = BookAdd(**data.model_dump(), author_id=user_id)
        book = await self.db.books.add(new_data)
        await self.db.commit()
        return book

    async def edit_book(self, book_id: int, data: BookAddRequest, user_id: int):
        book = await self.get_book(book_id)
        if book.author_id != user_id:
            raise HTTPException(status_code=404, detail="Вы не автор")
        await self.db.books.edit(data, id=book_id)
        await self.db.commit()

    async def edit_book_partially(self, book_id: int, data: BookPatch, user_id: int):
        book = await self.get_book(book_id)
        if book.author_id != user_id:
            raise HTTPException(status_code=404, detail="Вы не автор")
        await self.db.books.edit(data, exclude_unset=True, id=book_id)
        await self.db.commit()
