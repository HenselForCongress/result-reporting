# don/views/__init__.py
from flask import Blueprint

# Import blueprints from other view files
from .results import results_blueprint
from .admin import admin_blueprint

# Initialize a new Blueprint object if needed
main_blueprint = Blueprint('main', __name__)

# List of blueprints to be registered in the main app
blueprints = [results_blueprint, admin_blueprint]