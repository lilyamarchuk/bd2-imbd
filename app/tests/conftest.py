import pytest
from sqlalchemy import event
from sqlalchemy.engine import Engine

from my_project import create_app
from my_project.utils.db import db


@event.listens_for(Engine, "connect")
def _sqlite_fk(dbapi_conn, _):
    try:
        dbapi_conn.execute("PRAGMA foreign_keys=ON")
    except Exception:
        pass


@pytest.fixture()
def client():
    cfg = {"app": {}, "database": {}}
    app = create_app(config=cfg, db_uri="sqlite:///:memory:")
    app.config["TESTING"] = True
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()
