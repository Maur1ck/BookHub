from datetime import datetime, timezone, timedelta

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from app.core.config import settings
from app.models.users import RoleName
from app.schemas.users import UserAddRequest, UserAdd
from app.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str):
        return self.pwd_context.verify(password, hashed_password)

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def decode_token(self, token: str):
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])

    async def register_user(self, data: UserAddRequest):
        hashed_password = self.hash_password(data.password)
        user_data = UserAdd(email=data.email, hashed_password=hashed_password, role=RoleName.USER)
        try:
            await self.db.users.add(user_data)
            await self.db.commit()
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Пользователь с такой почтой уже существует")

    async def login_user(self, data: UserAddRequest):
        user = await self.db.users.get_user_with_hashed_pasword(data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
        if not self.verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")
        access_token = self.create_access_token({"user_id": user.id})
        return access_token

    async def get_one_or_none_user(self, user_id: int):
        return await self.db.users.get_one_or_none(id=user_id)
