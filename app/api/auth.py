from fastapi import APIRouter, HTTPException, Response
from sqlalchemy.exc import IntegrityError

from app.api.dependencies import DBDep, UserIdDep
from app.models.users import RoleName
from app.schemas.users import UserRequestAdd, UserAdd
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Аутентификация и вторизация"])


@router.post("/register")
async def register_user(data: UserRequestAdd, db: DBDep):
    hashed_password = AuthService().hash_password(data.password)
    user_data = UserAdd(email=data.email, hashed_password=hashed_password, role=RoleName.USER)
    try:
        await db.users.add(user_data)
        await db.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Пользователь с такой почтой уже существует")
    return {"status": "OK"}


@router.post("/login")
async def login_user(data: UserRequestAdd, response: Response, db: DBDep):
    user = await db.users.get_user_with_hashed_pasword(data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Пароль неверный")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie(key="access_token", value=access_token)
    return {"access_token": access_token}


@router.post("/logout")
def logout_user(response: Response):
    response.delete_cookie(key="access_token")
    return {"status": "OK", "message": "Logged out"}


@router.get("/me")
async def get_me(user_id: UserIdDep, db: DBDep):
    return await db.users.get_one_or_none(id=user_id)
