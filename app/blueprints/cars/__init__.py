from flask import Blueprint

bp = Blueprint('cars', __name__)

from app.blueprints.cars import routes