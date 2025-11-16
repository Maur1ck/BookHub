from pydantic import BaseModel
from sqlalchemy import select, insert
from sqlalchemy.exc import NoResultFound

from app.exceptions import ObjectNotFoundException


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self):
        query = select(self.model)
        results = await self.session.execute(query)
        model = results.scalars().all()
        return model

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
