from dao.base import BaseDAO
from users.model import Users


class UsersDAO(BaseDAO):
    model = Users
