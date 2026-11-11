from flask import jsonify

from my_project.auth.controller.base_controller import BaseController
from my_project.auth.service.rating_service import RatingService


class RatingController(BaseController):
    def __init__(self):
        super().__init__(RatingService())

    def get_average(self, movie_id):
        return jsonify(self.service.get_average(movie_id))
