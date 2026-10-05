from flask import Flask

from .config import Config
from .extensions import init_db
from .routes.health import health_bp
from .routes.services import services_bp


def create_app():
    # Flask uses this package's location to find resources such as templates and static files.
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(services_bp)
    return app
