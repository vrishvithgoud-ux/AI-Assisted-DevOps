from flask import Flask

from .config import Config
from .routes.health import health_bp
from .routes.services import services_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(health_bp)
    app.register_blueprint(services_bp)

    return app

