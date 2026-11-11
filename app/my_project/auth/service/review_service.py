from datetime import date

from my_project.auth.dao.movie_dao import MovieDAO
from my_project.auth.dao.review_dao import ReviewDAO
from my_project.auth.service.base_service import BaseService
from my_project.auth.service.helpers import parse_dates_in, parse_date
from my_project.utils.errors import ApiError


class ReviewService(BaseService):
    dao = ReviewDAO()
    label = "Відгук"
    required = ("movie_id", "author_name", "review_text")

    def get_all(self, date_from=None, date_to=None):
        if date_from and date_to:
            return self.dao.find_between(parse_date(date_from, "from"), parse_date(date_to, "to"))
        return self.dao.find_all()

    def prepare(self, data):
        data.setdefault("review_date", date.today())
        return parse_dates_in(data, ("review_date",))

    def update(self, item_id, data):
        return super().update(item_id, parse_dates_in(data, ("review_date",)))

    def validate(self, data):
        if "movie_id" in data and MovieDAO().find_by_id(data["movie_id"]) is None:
            raise ApiError(f"Фільм з id={data['movie_id']} не існує", 400)
