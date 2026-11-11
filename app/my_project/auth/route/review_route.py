from my_project.auth.controller.review_controller import ReviewController
from my_project.auth.route.base_route import create_crud_blueprint

review_bp = create_crud_blueprint("reviews", "/api/reviews", ReviewController())
