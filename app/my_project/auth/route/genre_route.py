from my_project.auth.controller.genre_controller import GenreController
from my_project.auth.route.base_route import create_crud_blueprint

controller = GenreController()
genre_bp = create_crud_blueprint("genres", "/api/genres", controller)

genre_bp.add_url_rule("/<int:item_id>/movies", "movies", controller.get_movies, methods=["GET"])
