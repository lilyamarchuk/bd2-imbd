from my_project.auth.controller.country_controller import CountryController
from my_project.auth.route.base_route import create_crud_blueprint

controller = CountryController()
country_bp = create_crud_blueprint("countries", "/api/countries", controller)
country_bp.add_url_rule("/<int:item_id>/movies", "movies", controller.get_movies, methods=["GET"])
country_bp.add_url_rule("/<int:item_id>/box-office", "box_office", controller.get_box_office, methods=["GET"])
