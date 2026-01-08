from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import NoResultFound

from app.core.exceptions import ObjectNotFoundException


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, limit: int | None = None, offset: int | None = None, **filters):
        query = select(self.model).filter(*filter).filter_by(**filters)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        result = await self.session.execute(query)
        model = result.scalars().all()
        return model

    async def get_all(self, limit: int | None = None, offset: int | None = None, **filters):
        return await self.get_filtered(limit=limit, offset=offset, **filters)

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

    async def edit(self, data: BaseModel, exclude_unset=False, **filters):
        stmt = (
            update(self.model)
            .filter_by(**filters)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(stmt)

    async def delete(self, **filters):
        delete_data_stmt = delete(self.model).filter_by(**filters)
        await self.session.execute(delete_data_stmt)
