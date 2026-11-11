from datetime import date

from my_project.auth.dao.box_office_dao import BoxOfficeDAO
from my_project.auth.dao.country_dao import CountryDAO
from my_project.auth.dao.genre_dao import GenreDAO
from my_project.auth.dao.movie_cast_dao import MovieCastDAO
from my_project.auth.dao.movie_dao import MovieDAO
from my_project.auth.dao.rating_dao import RatingDAO
from my_project.auth.dao.review_dao import ReviewDAO
from my_project.auth.dao.trivia_dao import TriviaDAO
from my_project.auth.service.base_service import BaseService
from my_project.utils.errors import ApiError


class MovieService(BaseService):
    dao = MovieDAO()
    label = "Фільм"
    required = ("title", "release_year")

    def get_all(self, title=None, year=None, genre_id=None):
        if title or year or genre_id:
            return self.dao.search(title, year, genre_id)
        return self.dao.find_all()

    def validate(self, data):
        if "release_year" in data:
            y = data["release_year"]
            if not isinstance(y, int) or not 1888 <= y <= date.today().year + 5:
                raise ApiError("release_year має бути цілим числом від 1888 до поточного року + 5", 400)
        if "duration_min" in data and data["duration_min"] is not None:
            d = data["duration_min"]
            if not isinstance(d, int) or d <= 0:
                raise ApiError("duration_min має бути додатним цілим числом", 400)

    def get_genres(self, movie_id):
        return self.get_by_id(movie_id).genres

    def add_genre(self, movie_id, genre_id):
        movie = self.get_by_id(movie_id)
        genre = GenreDAO().find_by_id(genre_id)
        if genre is None:
            raise ApiError(f"Жанр з id={genre_id} не знайдено", 404)
        self.dao.add_genre(movie, genre)
        return movie.genres

    def remove_genre(self, movie_id, genre_id):
        movie = self.get_by_id(movie_id)
        genre = GenreDAO().find_by_id(genre_id)
        if genre is None or genre not in movie.genres:
            raise ApiError("Фільм не має такого жанру", 404)
        self.dao.remove_genre(movie, genre)

    def get_countries(self, movie_id):
        return self.get_by_id(movie_id).countries

    def add_country(self, movie_id, country_id):
        movie = self.get_by_id(movie_id)
        country = CountryDAO().find_by_id(country_id)
        if country is None:
            raise ApiError(f"Країна з id={country_id} не знайдена", 404)
        self.dao.add_country(movie, country)
        return movie.countries

    def remove_country(self, movie_id, country_id):
        movie = self.get_by_id(movie_id)
        country = CountryDAO().find_by_id(country_id)
        if country is None or country not in movie.countries:
            raise ApiError("Фільм не пов'язаний із такою країною", 404)
        self.dao.remove_country(movie, country)

    def get_cast(self, movie_id):
        self.get_by_id(movie_id)
        return MovieCastDAO().find_by_movie(movie_id)

    def get_reviews(self, movie_id):
        self.get_by_id(movie_id)
        return ReviewDAO().find_by_movie(movie_id)

    def get_ratings(self, movie_id):
        self.get_by_id(movie_id)
        return RatingDAO().find_by_movie(movie_id)

    def get_trivia(self, movie_id):
        self.get_by_id(movie_id)
        return TriviaDAO().find_by_movie(movie_id)

    def get_box_office(self, movie_id):
        self.get_by_id(movie_id)
        return BoxOfficeDAO().find_by_movie(movie_id)

    def get_details(self, movie_id):
        movie = self.get_by_id(movie_id)
        avg, votes = RatingDAO().average_for_movie(movie_id)
        dto = movie.to_dto()
        dto["genres"] = [g.name for g in movie.genres]
        dto["countries"] = [c.name for c in movie.countries]
        dto["cast"] = [
            {"person": c.person.full_name, "role": c.role.role_name, "character": c.character_name}
            for c in MovieCastDAO().find_by_movie(movie_id)
        ]
        dto["average_rating"] = avg
        dto["votes"] = votes
        dto["reviews_count"] = len(movie.reviews)
        dto["box_office_total_usd"] = BoxOfficeDAO().total_for_movie(movie_id)
        return dto

    def get_top_rated(self, limit=5):
        if limit < 1 or limit > 50:
            raise ApiError("limit має бути в межах 1..50", 400)
        result = []
        for movie, avg, votes in self.dao.top_rated(limit):
            dto = movie.to_dto()
            dto["average_rating"] = round(float(avg), 2)
            dto["votes"] = votes
            result.append(dto)
        return result
