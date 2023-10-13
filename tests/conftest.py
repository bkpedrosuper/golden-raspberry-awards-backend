import pytest
from app.server.instance import Server
from app.extensions.db import db

from app.db_files.db_utils import populate_db

@pytest.fixture()
def app():
    server = Server(database_uri="sqlite://")
    app = server.app

    db.init_app(app)
    with app.app_context():
        db.create_all()
    populate_db(db, app, True)

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()