from my_project.auth.dao.base_dao import BaseDAO
from my_project.auth.domain import Review


class ReviewDAO(BaseDAO):
    model = Review

    def find_by_movie(self, movie_id):
        return Review.query.filter_by(movie_id=movie_id).order_by(Review.review_date.desc()).all()

    def find_between(self, date_from, date_to):
        return Review.query.filter(Review.review_date.between(date_from, date_to)).all()
