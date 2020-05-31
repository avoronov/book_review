import os
from sanic import Sanic

from blueprints import get_blueprints
from models import db


app = Sanic("books_review")

app.config.update({
    "DB_HOST": os.getenv("DB_HOST", "0.0.0.0"),
    "DB_PORT": os.getenv("DB_PORT", 5432),
    "DB_USER": os.getenv("DB_USER", "postgres"),
    "DB_PASSWORD": os.getenv("DB_PASS", "postgres"),
    "DB_DATABASE": os.getenv("DB_NAME", "postgres"),
    "DB_KWARGS": dict(
        max_inactive_connection_lifetime=59.0,
    ),
    "DB_ECHO": True
})

for blueprint in get_blueprints():
    app.blueprint(blueprint)

db.init_app(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
