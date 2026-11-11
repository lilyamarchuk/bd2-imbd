from flask import Blueprint, jsonify

ui_bp = Blueprint("ui", __name__)


@ui_bp.route("/")
def index():
    return jsonify({
        "project": "imdb_lab back-end (Flask + MySQL)",
        "resources": ["/api/genres", "/api/countries", "/api/persons", "/api/roles", "/api/movies",
                      "/api/cast", "/api/reviews", "/api/ratings", "/api/trivia", "/api/box-office"],
    })
