from my_project.auth.dao.base_dao import BaseDAO
from my_project.auth.domain import Role


class RoleDAO(BaseDAO):
    model = Role
