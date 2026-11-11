from my_project.auth.controller.rating_controller import RatingController
from my_project.auth.route.base_route import create_crud_blueprint

controller = RatingController()
rating_bp = create_crud_blueprint("ratings", "/api/ratings", controller)
rating_bp.add_url_rule("/movie/<int:movie_id>/average", "average", controller.get_average, methods=["GET"])
