from my_project.auth.controller.box_office_controller import BoxOfficeController
from my_project.auth.route.base_route import create_crud_blueprint

box_office_bp = create_crud_blueprint("box_office", "/api/box-office", BoxOfficeController())
