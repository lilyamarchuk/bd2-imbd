from my_project.auth.route.genre_route import genre_bp
from my_project.auth.route.country_route import country_bp
from my_project.auth.route.person_route import person_bp
from my_project.auth.route.role_route import role_bp
from my_project.auth.route.movie_route import movie_bp
from my_project.auth.route.movie_cast_route import cast_bp
from my_project.auth.route.review_route import review_bp
from my_project.auth.route.rating_route import rating_bp
from my_project.auth.route.trivia_route import trivia_bp
from my_project.auth.route.box_office_route import box_office_bp


def register_routes(app):
    for bp in (genre_bp, country_bp, person_bp, role_bp, movie_bp, cast_bp,
               review_bp, rating_bp, trivia_bp, box_office_bp):
        app.register_blueprint(bp)
