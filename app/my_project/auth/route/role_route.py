from my_project.auth.controller.role_controller import RoleController
from my_project.auth.route.base_route import create_crud_blueprint

controller = RoleController()
role_bp = create_crud_blueprint("roles", "/api/roles", controller)
role_bp.add_url_rule("/<int:item_id>/cast", "cast", controller.get_cast, methods=["GET"])
