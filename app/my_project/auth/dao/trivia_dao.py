from my_project.auth.dao.base_dao import BaseDAO
from my_project.auth.domain import Trivia


class TriviaDAO(BaseDAO):
    model = Trivia

    def find_by_movie(self, movie_id):
        return Trivia.query.filter_by(movie_id=movie_id).all()
