from my_project.auth.dao.movie_cast_dao import MovieCastDAO
from my_project.auth.dao.person_dao import PersonDAO
from my_project.auth.service.base_service import BaseService
from my_project.auth.service.helpers import parse_dates_in


class PersonService(BaseService):
    dao = PersonDAO()
    label = "Особа"
    required = ("full_name",)

    def get_all(self, name=None):
        return self.dao.search_by_name(name) if name else self.dao.find_all()

    def prepare(self, data):
        return parse_dates_in(data, ("birth_date",))

    def update(self, item_id, data):
        return super().update(item_id, parse_dates_in(data, ("birth_date",)))

    def get_filmography(self, person_id):
        self.get_by_id(person_id)
        return MovieCastDAO().find_by_person(person_id)
