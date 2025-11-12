from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from app.api.dependencies import DBDep
from app.schemas.users import UserRequestAdd, UserAdd
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Аутентификация и вторизация"])


@router.post("/register")
async def register_user(data: UserRequestAdd, db: DBDep):
    try:
        hashed_password = AuthService().hash_password(data.password)
        user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        await db.users.add(user_data)
        await db.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Пользователь с такой почтой уже существует")
    return {"status": "OK"}
