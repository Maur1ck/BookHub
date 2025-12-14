from typing import Annotated

from fastapi import Depends, Request, HTTPException
from jwt import ExpiredSignatureError

from app.core.database import async_session_maker
from app.models.users import UsersOrm, RoleName
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


async def get_current_user(user_id: UserIdDep, db: DBDep):
    user = await db.users.get_one_or_none(id=user_id)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Пользователь не найден",
        )
    return user

CurrentUserDep = Annotated[UsersOrm, Depends(get_current_user)]


async def admin_required(current_user: CurrentUserDep) -> UsersOrm:
    if current_user.role != RoleName.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Доступ разрешён только администратору",
        )
    return current_user

AdminDep = Annotated[UsersOrm, Depends(admin_required)]


async def author_or_admin_required(current_user: CurrentUserDep) -> UsersOrm:
    if current_user.role not in (RoleName.ADMIN, RoleName.AUTHOR):
        raise HTTPException(
            status_code=403,
            detail="Нужно быть автором или администратором",
        )
    return current_user

AuthorOrAdminDep = Annotated[UsersOrm, Depends(author_or_admin_required)]
