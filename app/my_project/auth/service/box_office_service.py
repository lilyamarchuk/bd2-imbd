from my_project.auth.dao.box_office_dao import BoxOfficeDAO
from my_project.auth.dao.country_dao import CountryDAO
from my_project.auth.dao.movie_dao import MovieDAO
from my_project.auth.service.base_service import BaseService
from my_project.utils.errors import ApiError


class BoxOfficeService(BaseService):
    dao = BoxOfficeDAO()
    label = "Запис про касові збори"
    required = ("movie_id", "country_id", "amount_usd")

    def validate(self, data):
        if "amount_usd" in data:
            try:
                ok = float(data["amount_usd"]) >= 0
            except (TypeError, ValueError):
                ok = False
            if not ok:
                raise ApiError("amount_usd має бути невід'ємним числом", 400)
        if "movie_id" in data and MovieDAO().find_by_id(data["movie_id"]) is None:
            raise ApiError(f"Фільм з id={data['movie_id']} не існує", 400)
        if "country_id" in data and CountryDAO().find_by_id(data["country_id"]) is None:
            raise ApiError(f"Країна з id={data['country_id']} не існує", 400)
