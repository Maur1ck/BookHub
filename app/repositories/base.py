from sqlalchemy import select


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self):
        query = select(self.model)
        results = await self.session.execute(query)
        return results.scalars().all()
