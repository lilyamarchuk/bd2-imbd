from my_project.auth.dao.base_dao import BaseDAO
from my_project.auth.domain import Genre


class GenreDAO(BaseDAO):
    model = Genre

    def find_by_name(self, name):
        return Genre.query.filter_by(name=name).first()
