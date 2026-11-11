from my_project.auth.dao.movie_dao import MovieDAO
from my_project.auth.dao.movie_cast_dao import MovieCastDAO
from my_project.auth.dao.person_dao import PersonDAO
from my_project.auth.dao.role_dao import RoleDAO
from my_project.auth.service.base_service import BaseService
from my_project.utils.errors import ApiError


class MovieCastService(BaseService):
    dao = MovieCastDAO()
    label = "Запис про участь"
    required = ("movie_id", "person_id", "role_id")

    def validate(self, data):
        for field, dao, name in (("movie_id", MovieDAO(), "Фільм"),
                                 ("person_id", PersonDAO(), "Особа"),
                                 ("role_id", RoleDAO(), "Роль")):
            if field in data and dao.find_by_id(data[field]) is None:
                raise ApiError(f"{name} з id={data[field]} не існує", 400)
