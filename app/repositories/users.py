from app.models.users import UsersOrm
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    model = UsersOrm
