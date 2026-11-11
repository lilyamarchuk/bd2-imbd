from my_project.auth.controller.movie_controller import MovieController
from my_project.auth.route.base_route import create_crud_blueprint

controller = MovieController()
movie_bp = create_crud_blueprint("movies", "/api/movies", controller)

movie_bp.add_url_rule("/top", "top", controller.get_top, methods=["GET"])
movie_bp.add_url_rule("/<int:item_id>/details", "details", controller.get_details, methods=["GET"])


movie_bp.add_url_rule("/<int:item_id>/genres", "genres", controller.get_genres, methods=["GET"])
movie_bp.add_url_rule("/<int:item_id>/genres/<int:genre_id>", "add_genre", controller.add_genre, methods=["POST"])
movie_bp.add_url_rule("/<int:item_id>/genres/<int:genre_id>", "remove_genre", controller.remove_genre, methods=["DELETE"])


movie_bp.add_url_rule("/<int:item_id>/countries", "countries", controller.get_countries, methods=["GET"])
movie_bp.add_url_rule("/<int:item_id>/countries/<int:country_id>", "add_country", controller.add_country, methods=["POST"])
movie_bp.add_url_rule("/<int:item_id>/countries/<int:country_id>", "remove_country", controller.remove_country, methods=["DELETE"])


movie_bp.add_url_rule("/<int:item_id>/cast", "cast", controller.get_cast, methods=["GET"])
movie_bp.add_url_rule("/<int:item_id>/reviews", "reviews", controller.get_reviews, methods=["GET"])
movie_bp.add_url_rule("/<int:item_id>/ratings", "ratings", controller.get_ratings, methods=["GET"])
movie_bp.add_url_rule("/<int:item_id>/trivia", "trivia", controller.get_trivia, methods=["GET"])
movie_bp.add_url_rule("/<int:item_id>/box-office", "box_office", controller.get_box_office, methods=["GET"])
