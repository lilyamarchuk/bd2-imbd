from my_project.auth.controller.person_controller import PersonController
from my_project.auth.route.base_route import create_crud_blueprint

controller = PersonController()
person_bp = create_crud_blueprint("persons", "/api/persons", controller)

person_bp.add_url_rule("/<int:item_id>/filmography", "filmography", controller.get_filmography, methods=["GET"])
