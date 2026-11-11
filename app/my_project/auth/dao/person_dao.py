from my_project.auth.dao.base_dao import BaseDAO
from my_project.auth.domain import Person


class PersonDAO(BaseDAO):
    model = Person

    def search_by_name(self, name):
        return Person.query.filter(Person.full_name.like(f"%{name}%")).order_by(Person.full_name).all()
