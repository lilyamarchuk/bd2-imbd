from my_project.auth.dao.movie_dao import MovieDAO
from my_project.auth.dao.trivia_dao import TriviaDAO
from my_project.auth.service.base_service import BaseService
from my_project.utils.errors import ApiError


class TriviaService(BaseService):
    dao = TriviaDAO()
    label = "Цікавий факт"
    required = ("movie_id", "fact_text")

    def validate(self, data):
        if "movie_id" in data and MovieDAO().find_by_id(data["movie_id"]) is None:
            raise ApiError(f"Фільм з id={data['movie_id']} не існує", 400)
