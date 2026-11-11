from my_project.auth.controller.base_controller import BaseController, dto_list
from my_project.auth.service.genre_service import GenreService


class GenreController(BaseController):
    def __init__(self):
        super().__init__(GenreService())

    def get_movies(self, item_id):
        return dto_list(self.service.get_movies(item_id))
