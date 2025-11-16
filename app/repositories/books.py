from app.models.books import BooksOrm
from app.repositories.base import BaseRepository


class BooksRepository(BaseRepository):
    model = BooksOrm
