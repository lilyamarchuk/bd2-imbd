from flask import jsonify, request

from my_project.auth.controller.base_controller import BaseController, dto_list
from my_project.auth.service.movie_service import MovieService
from my_project.utils.errors import ApiError


class MovieController(BaseController):
    def __init__(self):
        super().__init__(MovieService())

    def get_all(self):
        year = request.args.get("year", type=int)
        genre_id = request.args.get("genre_id", type=int)
        return dto_list(self.service.get_all(request.args.get("title"), year, genre_id))

    def get_details(self, item_id):
        return jsonify(self.service.get_details(item_id))

    def get_top(self):
        limit = request.args.get("limit", default=5, type=int)
        return jsonify(self.service.get_top_rated(limit))

    def get_genres(self, item_id):
        return dto_list(self.service.get_genres(item_id))

    def add_genre(self, item_id, genre_id):
        return dto_list(self.service.add_genre(item_id, genre_id)), 201

    def remove_genre(self, item_id, genre_id):
        self.service.remove_genre(item_id, genre_id)
        return jsonify({"message": "Жанр відв'язано від фільму"})

    def get_countries(self, item_id):
        return dto_list(self.service.get_countries(item_id))

    def add_country(self, item_id, country_id):
        return dto_list(self.service.add_country(item_id, country_id)), 201

    def remove_country(self, item_id, country_id):
        self.service.remove_country(item_id, country_id)
        return jsonify({"message": "Країну відв'язано від фільму"})

    def get_cast(self, item_id):
        return dto_list(self.service.get_cast(item_id))

    def get_reviews(self, item_id):
        return dto_list(self.service.get_reviews(item_id))

    def get_ratings(self, item_id):
        return dto_list(self.service.get_ratings(item_id))

    def get_trivia(self, item_id):
        return dto_list(self.service.get_trivia(item_id))

    def get_box_office(self, item_id):
        return dto_list(self.service.get_box_office(item_id))
