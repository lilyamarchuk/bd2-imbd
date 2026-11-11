from my_project.auth.controller.base_controller import BaseController
from my_project.auth.service.movie_cast_service import MovieCastService


class MovieCastController(BaseController):
    def __init__(self):
        super().__init__(MovieCastService())
