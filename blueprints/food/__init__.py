from flask import Blueprint

food_bp = Blueprint('food', __name__, template_folder='../../templates/food')

from . import routes  # noqa
