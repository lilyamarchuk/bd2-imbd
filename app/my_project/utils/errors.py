from flask import jsonify
from sqlalchemy.exc import IntegrityError, DataError


class ApiError(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.message = message
        self.status = status


def register_error_handlers(app):
    from my_project.utils.db import db

    @app.errorhandler(ApiError)
    def handle_api_error(e):
        return jsonify({"error": e.message}), e.status

    @app.errorhandler(IntegrityError)
    def handle_integrity(e):
        db.session.rollback()
        return jsonify({"error": "Порушення цілісності даних (дублікат, неіснуючий зовнішній ключ "
                                 "або запис використовується в інших таблицях)",
                        "details": str(e.orig)}), 409

    @app.errorhandler(DataError)
    def handle_data(e):
        db.session.rollback()
        return jsonify({"error": "Некоректне значення поля", "details": str(e.orig)}), 400

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({"error": "Ресурс не знайдено"}), 404

    @app.errorhandler(405)
    def handle_405(e):
        return jsonify({"error": "Метод не дозволений"}), 405
