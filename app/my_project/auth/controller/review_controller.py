from flask import request

from my_project.auth.controller.base_controller import BaseController, dto_list
from my_project.auth.service.review_service import ReviewService


class ReviewController(BaseController):
    def __init__(self):
        super().__init__(ReviewService())

    def get_all(self):
        return dto_list(self.service.get_all(request.args.get("from"), request.args.get("to")))
