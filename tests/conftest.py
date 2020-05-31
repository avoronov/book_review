import os
import pytest

from alembic.config import main
from sanic import Sanic

from blueprints import get_blueprints
from models import db


@pytest.yield_fixture
def app():
    app = Sanic("books_review_test")

    app.config.update({
        "DB_HOST": os.getenv("DB_HOST", "0.0.0.0"),
        "DB_PORT": os.getenv("DB_PORT", 5432),
        "DB_USER": os.getenv("DB_USER", "postgres"),
        "DB_PASSWORD": os.getenv("DB_PASS", "postgres"),
        "DB_DATABASE": "_".join([os.getenv("DB_NAME", "postgres"), "test"]),
        "DB_KWARGS": dict(
            max_inactive_connection_lifetime=59.0,
        ),
        "DB_ECHO": True
    })

    for blueprint in get_blueprints():
        app.blueprint(blueprint)

    db.init_app(app)

    main(["--raiseerr", "upgrade", "head"])
    yield app
    main(["--raiseerr", "downgrade", "base"])


@pytest.fixture
def test_cli(loop, app, sanic_client):
    return loop.run_until_complete(sanic_client(app))
