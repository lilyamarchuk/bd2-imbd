from sqlalchemy import func

from my_project.auth.dao.base_dao import BaseDAO
from my_project.auth.domain import Rating
from my_project.utils.db import db


class RatingDAO(BaseDAO):
    model = Rating

    def find_by_movie(self, movie_id):
        return Rating.query.filter_by(movie_id=movie_id).order_by(Rating.rating_date).all()

    def find_by_movie_and_user(self, movie_id, user_name):
        return Rating.query.filter_by(movie_id=movie_id, user_name=user_name).first()

    def average_for_movie(self, movie_id):
        avg, cnt = db.session.query(func.avg(Rating.score), func.count(Rating.rating_id)) \
            .filter(Rating.movie_id == movie_id).one()
        return (round(float(avg), 2) if avg is not None else None), cnt
