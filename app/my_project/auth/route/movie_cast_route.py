from my_project.auth.controller.movie_cast_controller import MovieCastController
from my_project.auth.route.base_route import create_crud_blueprint

cast_bp = create_crud_blueprint("movie_cast", "/api/cast", MovieCastController())
