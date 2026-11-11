from my_project.auth.dao.base_dao import BaseDAO
from my_project.auth.domain import MovieCast


class MovieCastDAO(BaseDAO):
    model = MovieCast

    def find_by_movie(self, movie_id):
        return MovieCast.query.filter_by(movie_id=movie_id).order_by(MovieCast.role_id, MovieCast.cast_id).all()

    def find_by_person(self, person_id):
        return MovieCast.query.filter_by(person_id=person_id).order_by(MovieCast.movie_id).all()

    def find_by_role(self, role_id):
        return MovieCast.query.filter_by(role_id=role_id).order_by(MovieCast.movie_id).all()
