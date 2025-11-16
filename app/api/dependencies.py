from typing import Annotated

from fastapi import Depends, Request, HTTPException
from jwt import ExpiredSignatureError

from app.core.database import async_session_maker
from app.services.auth import AuthService
from app.utils.db_manager import DBManager


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db

DBDep = Annotated[DBManager, Depends(get_db)]


def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен")
    return token


def get_current_user_id(token: str = Depends(get_token)):
    try:
        data = AuthService().decode_token(token)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Срок действия вашего JWT токена истек.")
    return data.get("user_id")


UserIdDep = Annotated[int, Depends(get_current_user_id)]
