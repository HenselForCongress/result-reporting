# don/__init__.py
from .utils import logger, configure_logger
from flask import Flask
from .views import blueprints

def create_app():
    app = Flask(__name__)

    # Register all blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app