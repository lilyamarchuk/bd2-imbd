from datetime import date

from my_project.auth.dao.movie_dao import MovieDAO
from my_project.auth.dao.rating_dao import RatingDAO
from my_project.auth.service.base_service import BaseService
from my_project.auth.service.helpers import parse_dates_in
from my_project.utils.errors import ApiError


class RatingService(BaseService):
    dao = RatingDAO()
    label = "Оцінка"
    required = ("movie_id", "user_name", "score")

    def prepare(self, data):
        data.setdefault("rating_date", date.today())
        return parse_dates_in(data, ("rating_date",))

    def update(self, item_id, data):
        return super().update(item_id, parse_dates_in(data, ("rating_date",)))

    def validate(self, data):
        if "score" in data:
            try:
                score = float(data["score"])
            except (TypeError, ValueError):
                raise ApiError("score має бути числом", 400)
            if not 0 <= score <= 10:
                raise ApiError("score має бути в межах від 0 до 10", 400)
        if "movie_id" in data:
            if MovieDAO().find_by_id(data["movie_id"]) is None:
                raise ApiError(f"Фільм з id={data['movie_id']} не існує", 400)

    def create(self, data):

        if data.get("movie_id") and data.get("user_name") and \
                self.dao.find_by_movie_and_user(data["movie_id"], data["user_name"]):
            raise ApiError("Цей користувач уже оцінив цей фільм (використайте PUT для зміни оцінки)", 409)
        return super().create(data)

    def get_average(self, movie_id):
        if MovieDAO().find_by_id(movie_id) is None:
            raise ApiError(f"Фільм з id={movie_id} не знайдено", 404)
        avg, votes = self.dao.average_for_movie(movie_id)
        return {"movie_id": movie_id, "average_rating": avg, "votes": votes}
