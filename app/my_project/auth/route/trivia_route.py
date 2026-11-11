from my_project.auth.controller.trivia_controller import TriviaController
from my_project.auth.route.base_route import create_crud_blueprint

trivia_bp = create_crud_blueprint("trivia", "/api/trivia", TriviaController())
