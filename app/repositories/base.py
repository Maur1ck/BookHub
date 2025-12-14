from pydantic import BaseModel
from sqlalchemy import select, insert, update
from sqlalchemy.exc import NoResultFound

from app.core.exceptions import ObjectNotFoundException
from app.models.books import BooksOrm


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filters):
        query = select(self.model).filter(*filter).filter_by(**filters)
        result = await self.session.execute(query)
        model = result.scalars().all()
        return model

    async def get_all(self):
        return await self.get_filtered()

    async def get_one_or_none(self, **filters):
        query = select(self.model).filter_by(**filters)
        results = await self.session.execute(query)
        model = results.scalar_one_or_none()
        return model

    async def get_one(self, **filters):
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return model

    async def add(self, data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_stmt)
        model = result.scalar_one()
        return model

    async def update(self, book_id: int, data: BaseModel):
        stmt = update(self.model).where(BooksOrm.id==book_id).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        model = result.scalar_one()
        return model
