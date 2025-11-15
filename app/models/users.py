from enum import StrEnum

from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class RoleName(StrEnum):
    USER = "user"
    AUTHOR = "author"
    ADMIN = "admin"


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(200))

    role: Mapped[RoleName] = mapped_column(
        Enum(RoleName, name="role_name"),
        default=RoleName.USER,
        nullable=False,
    )
