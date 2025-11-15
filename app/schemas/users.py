from pydantic import BaseModel, EmailStr, field_validator


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if not value or not value.strip():
            raise ValueError("Пароль не может быть пустым")
        return value


class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str
    role: str


class User(BaseModel):
    id: int
    email: EmailStr


class UserWithHashedPassword(User):
    hashed_password: str
