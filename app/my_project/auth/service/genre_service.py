from my_project.auth.dao.genre_dao import GenreDAO
from my_project.auth.service.base_service import BaseService


class GenreService(BaseService):
    dao = GenreDAO()
    label = "Жанр"
    required = ("name",)

    def get_movies(self, genre_id):
        return self.get_by_id(genre_id).movies
