from fastapi import APIRouter, HTTPException, Response, Request

from app.api.dependencies import DBDep, CurrentUserDep
from app.schemas.users import UserAddRequest
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Аутентификация и вторизация"])


@router.post("/register")
async def register_user(data: UserAddRequest, db: DBDep):
    await AuthService(db).register_user(data)
    return {"status": "OK"}


@router.post("/login")
async def login_user(data: UserAddRequest, response: Response, db: DBDep):
    access_token = await AuthService(db).login_user(data)
    response.set_cookie(key="access_token", value=access_token)
    return {"access_token": access_token}


@router.post("/logout")
def logout_user(response: Response, request: Request):
    if request.cookies.get("access_token") is None:
        raise HTTPException(status_code=400, detail="Already logged out")
    response.delete_cookie(key="access_token")
    return {"status": "OK", "message": "Logged out"}


@router.get("/me")
async def get_me(current_user: CurrentUserDep):
    return current_user
