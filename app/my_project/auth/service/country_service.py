from my_project.auth.dao.box_office_dao import BoxOfficeDAO
from my_project.auth.dao.country_dao import CountryDAO
from my_project.auth.service.base_service import BaseService
from my_project.utils.errors import ApiError


class CountryService(BaseService):
    dao = CountryDAO()
    label = "Країна"
    required = ("name", "code")

    def prepare(self, data):
        if isinstance(data.get("code"), str):
            data["code"] = data["code"].upper()
        return data

    def validate(self, data):
        if "code" in data:
            code = data["code"]
            if not isinstance(code, str) or len(code) != 2 or not code.isalpha():
                raise ApiError("Код країни має складатися з 2 літер (ISO 3166-1 alpha-2)", 400)
            data["code"] = code.upper()

    def get_movies(self, country_id):
        return self.get_by_id(country_id).movies

    def get_box_office(self, country_id):
        self.get_by_id(country_id)
        return BoxOfficeDAO().find_by_country(country_id)
