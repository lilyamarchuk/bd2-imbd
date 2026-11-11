from my_project.auth.controller.base_controller import BaseController
from my_project.auth.service.trivia_service import TriviaService


class TriviaController(BaseController):
    def __init__(self):
        super().__init__(TriviaService())
