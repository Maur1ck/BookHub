from pydantic import EmailStr
from sqlalchemy import select

from app.models.users import UsersOrm
from app.repositories.base import BaseRepository
from app.schemas.users import UserWithHashedPassword


class UserRepository(BaseRepository):
    model = UsersOrm

    async def get_user_with_hashed_pasword(self, email: EmailStr):
        query = select(self.model).where(self.model.email == email)
        result = await self.session.execute(query)
        model =  result.scalars().first()
        if model is None:
            return None
        return UserWithHashedPassword.model_validate(model, from_attributes=True)
