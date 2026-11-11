from sqlalchemy import func

from my_project.auth.dao.base_dao import BaseDAO
from my_project.auth.domain import BoxOffice
from my_project.utils.db import db


class BoxOfficeDAO(BaseDAO):
    model = BoxOffice

    def find_by_movie(self, movie_id):
        return BoxOffice.query.filter_by(movie_id=movie_id).order_by(BoxOffice.amount_usd.desc()).all()

    def find_by_country(self, country_id):
        return BoxOffice.query.filter_by(country_id=country_id).order_by(BoxOffice.amount_usd.desc()).all()

    def total_for_movie(self, movie_id):
        total = db.session.query(func.sum(BoxOffice.amount_usd)).filter(BoxOffice.movie_id == movie_id).scalar()
        return float(total) if total is not None else 0.0
