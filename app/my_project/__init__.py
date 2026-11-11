from flask import Flask

from my_project.utils.config import load_config, build_db_uri
from my_project.utils.db import db
from my_project.utils.errors import register_error_handlers


def create_app(config=None, db_uri=None):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.json.ensure_ascii = False
    app.json.sort_keys = False

    cfg = config or load_config()
    app.config["APP_CONFIG"] = cfg
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri or build_db_uri(cfg)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from my_project.auth import domain
    from my_project.auth.route import register_routes
    from my_project.ui import ui_bp

    register_routes(app)
    app.register_blueprint(ui_bp)
    register_error_handlers(app)
    return app
