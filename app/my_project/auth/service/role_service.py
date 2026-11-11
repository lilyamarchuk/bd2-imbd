from my_project.auth.dao.movie_cast_dao import MovieCastDAO
from my_project.auth.dao.role_dao import RoleDAO
from my_project.auth.service.base_service import BaseService


class RoleService(BaseService):
    dao = RoleDAO()
    label = "Роль"
    required = ("role_name",)

    def get_cast(self, role_id):
        self.get_by_id(role_id)
        return MovieCastDAO().find_by_role(role_id)
