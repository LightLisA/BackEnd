from app.users.models import Users
from app.services_dao_repository.base import BaseDAO


# DAO - Data Access Object; Services; Patterns; Repository
class UsersDAO(BaseDAO):
    model = Users
