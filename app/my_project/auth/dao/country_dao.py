from my_project.auth.dao.base_dao import BaseDAO
from my_project.auth.domain import Country


class CountryDAO(BaseDAO):
    model = Country

    def find_by_code(self, code):
        return Country.query.filter_by(code=code).first()
