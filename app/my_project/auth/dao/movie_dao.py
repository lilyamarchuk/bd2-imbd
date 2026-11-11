from sqlalchemy import func

from my_project.auth.dao.base_dao import BaseDAO
from my_project.auth.domain import Movie, Genre, Rating
from my_project.utils.db import db


class MovieDAO(BaseDAO):
    model = Movie

    def search(self, title=None, year=None, genre_id=None):
        q = Movie.query
        if title:
            q = q.filter(Movie.title.like(f"%{title}%"))
        if year:
            q = q.filter(Movie.release_year == year)
        if genre_id:
            q = q.filter(Movie.genres.any(Genre.genre_id == genre_id))
        return q.order_by(Movie.title).all()

    def top_rated(self, limit=5):
        return (db.session.query(Movie, func.avg(Rating.score).label("avg_score"), func.count(Rating.rating_id))
                .join(Rating, Rating.movie_id == Movie.movie_id)
                .group_by(Movie.movie_id)
                .order_by(func.avg(Rating.score).desc())
                .limit(limit).all())

    def add_genre(self, movie, genre):
        if genre not in movie.genres:
            movie.genres.append(genre)
            db.session.commit()

    def remove_genre(self, movie, genre):
        if genre in movie.genres:
            movie.genres.remove(genre)
            db.session.commit()

    def add_country(self, movie, country):
        if country not in movie.countries:
            movie.countries.append(country)
            db.session.commit()

    def remove_country(self, movie, country):
        if country in movie.countries:
            movie.countries.remove(country)
            db.session.commit()
